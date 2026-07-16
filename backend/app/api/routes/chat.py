from fastapi import APIRouter

from app.schemas.chat import ChatRequest, ChatResponse, ChatResponseData
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


router = APIRouter(prefix="/chat", tags=["Chat"])


@router.post("", response_model=ChatResponse)
def create_chat_response(request: ChatRequest) -> ChatResponse:
    context = build_retrieval_context(request.message)

    if not context:
        return ChatResponse(
            success=True,
            message="No relevant product context found",
            data=ChatResponseData(answer=build_no_context_answer()),
        )

    prompt = build_rag_prompt(
        user_message=request.message,
        context=context,
    )

    try:
        answer = generate_chat_completion(prompt)
        response_message = "Chat response generated with RAG"
    except OpenAIServiceError as exc:
        response_message, answer = build_openai_error_fallback(exc.code)

    if not answer.strip():
        answer = build_empty_model_answer()
        response_message = "Empty model response"

    return ChatResponse(
        success=True,
        message=response_message,
        data=ChatResponseData(answer=answer),
    )