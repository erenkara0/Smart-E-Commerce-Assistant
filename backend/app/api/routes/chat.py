from fastapi import APIRouter

from app.schemas.chat import ChatRequest, ChatResponse, ChatResponseData
from app.services.retrieval_context_builder import build_retrieval_context


router = APIRouter(prefix="/chat", tags=["Chat"])


@router.post("", response_model=ChatResponse)
def create_chat_response(request: ChatRequest) -> ChatResponse:
    context = build_retrieval_context(request.message)

    if not context:
        answer = (
            "Bu soruyla ilgili ürün veri setinde eşleşen bir bilgi bulunamadı. "
            "Lütfen ürün adı, kategori, marka veya özellik belirterek tekrar deneyin."
        )
    else:
        answer = (
            "Kullanıcı mesajına göre ilgili ürün context'i oluşturuldu:\n\n"
            f"{context}"
        )

    return ChatResponse(
        success=True,
        message="Chat response generated with retrieval context",
        data=ChatResponseData(answer=answer),
    )