from uuid import uuid4

from fastapi import APIRouter

from app.core.config import settings
from app.schemas.chat import ChatRequest, ChatResponse, ChatResponseData
from app.services.conversation_context_builder import (
    build_conversation_history,
    build_retrieval_query,
)
from app.services.openai_client import (
    OpenAIServiceError,
    generate_chat_completion,
)
from app.services.rag_fallbacks import (
    build_empty_model_answer,
    build_no_context_answer,
    build_openai_error_fallback,
)
from app.services.rag_prompt_builder import build_rag_prompt
from app.services.retrieval_context_builder import build_retrieval_context
from app.services.session_memory_service import session_memory_service


router = APIRouter(prefix="/chat", tags=["Chat"])


@router.post("", response_model=ChatResponse)
def create_chat_response(request: ChatRequest) -> ChatResponse:
    session_id = request.session_id or str(uuid4())

    previous_messages = session_memory_service.get_recent_messages(
        session_id=session_id,
        limit=settings.session_memory_limit,
    )

    conversation_history = build_conversation_history(previous_messages)

    retrieval_query = build_retrieval_query(
        current_message=request.message,
        messages=previous_messages,
    )

    session_memory_service.save_message(
        session_id=session_id,
        role="user",
        content=request.message,
    )

    context = build_retrieval_context(retrieval_query)

    if not context:
        answer = build_no_context_answer()

        session_memory_service.save_message(
            session_id=session_id,
            role="assistant",
            content=answer,
        )

        return ChatResponse(
            success=True,
            message="No relevant product context found",
            data=ChatResponseData(
                session_id=session_id,
                answer=answer,
            ),
        )

    prompt = build_rag_prompt(
        user_message=request.message,
        context=context,
        conversation_history=conversation_history,
    )

    try:
        answer = generate_chat_completion(prompt)
        response_message = "Chat response generated with RAG"
    except OpenAIServiceError as exc:
        response_message, answer = build_openai_error_fallback(exc.code)

    if not answer.strip():
        answer = build_empty_model_answer()
        response_message = "Empty model response"

    session_memory_service.save_message(
        session_id=session_id,
        role="assistant",
        content=answer,
    )

    return ChatResponse(
        success=True,
        message=response_message,
        data=ChatResponseData(
            session_id=session_id,
            answer=answer,
        ),
    )