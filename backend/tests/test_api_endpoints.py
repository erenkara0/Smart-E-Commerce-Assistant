import pytest
from fastapi.testclient import TestClient

from app.api.routes import chat as chat_route


REQUIRED_PRODUCT_FIELDS = {
    "id",
    "name",
    "category",
    "brand",
    "price",
    "currency",
    "description",
    "features",
    "stock",
    "rating",
}


def test_root_endpoint_returns_success(
    client: TestClient,
) -> None:
    response = client.get("/")

    assert response.status_code == 200

    response_body = response.json()

    assert response_body["success"] is True
    assert response_body["message"] == "MikroAsistan API is running"
    assert response_body["data"] is None


def test_products_endpoint_returns_product_collection(
    client: TestClient,
) -> None:
    response = client.get("/products")

    assert response.status_code == 200

    response_body = response.json()
    products = response_body["data"]["products"]

    assert response_body["success"] is True
    assert response_body["message"] == "Products listed successfully"
    assert response_body["data"]["total"] == len(products)
    assert len(products) > 0


def test_products_contain_required_fields(
    client: TestClient,
) -> None:
    response = client.get("/products")

    assert response.status_code == 200

    products = response.json()["data"]["products"]
    first_product = products[0]

    assert REQUIRED_PRODUCT_FIELDS.issubset(first_product.keys())
    assert first_product["price"] > 0
    assert first_product["stock"] >= 0
    assert 0 <= first_product["rating"] <= 5


def test_valid_chat_request_returns_mocked_answer(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    expected_answer = "Test asistan yanıtı"
    expected_session_id = "test-session-api"

    monkeypatch.setattr(
        chat_route,
        "build_retrieval_context",
        lambda query: "Test ürün bağlamı",
    )
    monkeypatch.setattr(
        chat_route,
        "generate_chat_completion",
        lambda prompt: expected_answer,
    )

    response = client.post(
        "/chat",
        json={
            "message": "Oyun için laptop önerir misin?",
            "session_id": expected_session_id,
        },
    )

    assert response.status_code == 200

    response_body = response.json()

    assert response_body["success"] is True
    assert response_body["message"] == "Chat response generated with RAG"
    assert response_body["data"]["session_id"] == expected_session_id
    assert response_body["data"]["answer"] == expected_answer


def test_blank_chat_message_returns_validation_error(
    client: TestClient,
) -> None:
    response = client.post(
        "/chat",
        json={"message": "   "},
    )

    assert response.status_code == 422

    response_body = response.json()

    assert response_body["success"] is False
    assert isinstance(response_body["message"], str)
    assert "data" in response_body


def test_missing_chat_request_body_returns_validation_error(
    client: TestClient,
) -> None:
    response = client.post("/chat")

    assert response.status_code == 422

    response_body = response.json()

    assert response_body["success"] is False
    assert isinstance(response_body["message"], str)
    assert "data" in response_body