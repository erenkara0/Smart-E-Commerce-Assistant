from typing import Any
from uuid import UUID, uuid4

import pytest
from fastapi.testclient import TestClient

from app.api.routes import chat as chat_route
from app.services.openai_client import OpenAIServiceError
from app.services.rag_fallbacks import (
    build_empty_model_answer,
    build_no_context_answer,
    build_openai_error_fallback,
)


def configure_successful_chat_mocks(
    monkeypatch: pytest.MonkeyPatch,
    answer: str,
) -> None:
    monkeypatch.setattr(
        chat_route,
        "build_retrieval_context",
        lambda query: "Test ürün bağlamı",
    )
    monkeypatch.setattr(
        chat_route,
        "generate_chat_completion",
        lambda prompt: answer,
    )


def test_chat_generates_session_id_when_not_provided(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    configure_successful_chat_mocks(
        monkeypatch,
        answer="Otomatik oturum testi başarılı.",
    )

    response = client.post(
        "/chat",
        json={"message": "Bir laptop önerir misin?"},
    )

    assert response.status_code == 200

    response_body = response.json()
    generated_session_id = response_body["data"]["session_id"]

    assert response_body["success"] is True
    assert generated_session_id

    parsed_session_id = UUID(generated_session_id)

    assert str(parsed_session_id) == generated_session_id


def test_chat_reuses_existing_session_id(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    expected_session_id = f"existing-session-{uuid4()}"

    configure_successful_chat_mocks(
        monkeypatch,
        answer="Mevcut oturum testi başarılı.",
    )

    response = client.post(
        "/chat",
        json={
            "message": "Stokta laptop var mı?",
            "session_id": expected_session_id,
        },
    )

    assert response.status_code == 200
    assert response.json()["data"]["session_id"] == expected_session_id


def test_follow_up_request_receives_previous_messages(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    session_id = f"history-session-{uuid4()}"
    first_question = "ASUS laptop önerir misin?"
    first_answer = "ASUS TUF Gaming A15 önerilebilir."
    second_question = "Bunun stok durumu nedir?"
    second_answer = "Ürünün stok bilgisi bulunmaktadır."

    captured_histories: list[list[dict[str, Any]]] = []

    def capture_conversation_history(
        messages: list[dict[str, Any]],
    ) -> str:
        captured_histories.append(
            [dict(message) for message in messages]
        )
        return "Test konuşma geçmişi"

    generated_answers = iter([first_answer, second_answer])

    monkeypatch.setattr(
        chat_route,
        "build_conversation_history",
        capture_conversation_history,
    )
    monkeypatch.setattr(
        chat_route,
        "build_retrieval_context",
        lambda query: "Test ürün bağlamı",
    )
    monkeypatch.setattr(
        chat_route,
        "generate_chat_completion",
        lambda prompt: next(generated_answers),
    )

    first_response = client.post(
        "/chat",
        json={
            "message": first_question,
            "session_id": session_id,
        },
    )

    second_response = client.post(
        "/chat",
        json={
            "message": second_question,
            "session_id": session_id,
        },
    )

    assert first_response.status_code == 200
    assert second_response.status_code == 200
    assert len(captured_histories) == 2

    second_request_history = captured_histories[1]

    assert len(second_request_history) == 2
    assert second_request_history[0]["role"] == "user"
    assert second_request_history[0]["content"] == first_question
    assert second_request_history[1]["role"] == "assistant"
    assert second_request_history[1]["content"] == first_answer


def test_chat_returns_no_context_fallback(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def fail_if_openai_is_called(prompt: str) -> str:
        raise AssertionError(
            "OpenAI should not be called without retrieval context."
        )

    monkeypatch.setattr(
        chat_route,
        "build_retrieval_context",
        lambda query: "",
    )
    monkeypatch.setattr(
        chat_route,
        "generate_chat_completion",
        fail_if_openai_is_called,
    )

    response = client.post(
        "/chat",
        json={
            "message": "Veri setinde olmayan bir ürün sorusu",
            "session_id": f"no-context-session-{uuid4()}",
        },
    )

    assert response.status_code == 200

    response_body = response.json()

    assert response_body["success"] is True
    assert (
        response_body["message"]
        == "No relevant product context found"
    )
    assert (
        response_body["data"]["answer"]
        == build_no_context_answer()
    )


@pytest.mark.parametrize(
    "error_code",
    [
        "rate_limit",
        "timeout",
        "connection_error",
    ],
)
def test_chat_returns_openai_error_fallback(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
    error_code: str,
) -> None:
    expected_message, expected_answer = (
        build_openai_error_fallback(error_code)
    )

    def raise_openai_service_error(prompt: str) -> str:
        raise OpenAIServiceError(
            code=error_code,
            message=f"Simulated {error_code} error.",
        )

    monkeypatch.setattr(
        chat_route,
        "build_retrieval_context",
        lambda query: "Test ürün bağlamı",
    )
    monkeypatch.setattr(
        chat_route,
        "generate_chat_completion",
        raise_openai_service_error,
    )

    response = client.post(
        "/chat",
        json={
            "message": "Test ürünü hakkında bilgi verir misin?",
            "session_id": f"{error_code}-session-{uuid4()}",
        },
    )

    assert response.status_code == 200

    response_body = response.json()

    assert response_body["success"] is True
    assert response_body["message"] == expected_message
    assert response_body["data"]["answer"] == expected_answer


def test_chat_returns_empty_model_fallback(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(
        chat_route,
        "build_retrieval_context",
        lambda query: "Test ürün bağlamı",
    )
    monkeypatch.setattr(
        chat_route,
        "generate_chat_completion",
        lambda prompt: "   ",
    )

    response = client.post(
        "/chat",
        json={
            "message": "Bir ürün önerir misin?",
            "session_id": f"empty-answer-session-{uuid4()}",
        },
    )

    assert response.status_code == 200

    response_body = response.json()

    assert response_body["success"] is True
    assert response_body["message"] == "Empty model response"
    assert (
        response_body["data"]["answer"]
        == build_empty_model_answer()
    )