from fastapi import APIRouter

from app.schemas.chat import ChatRequest, ChatResponse, ChatResponseData

router = APIRouter(prefix="/chat", tags=["Chat"])


@router.post("", response_model=ChatResponse)
def create_chat_response(request: ChatRequest) -> ChatResponse:
    return ChatResponse(
        success=True,
        message="Chat response generated",
        data=ChatResponseData(
            answer=(
                "Şu anda temel chat endpoint’i çalışıyor. "
                f"Aldığım mesaj: {request.message}"
            ),
        ),
    )