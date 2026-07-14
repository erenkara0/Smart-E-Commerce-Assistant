from fastapi import APIRouter

from app.schemas.chat import ChatRequest, ChatResponse, ChatResponseData
from app.services.openai_client import generate_chat_completion
from app.services.rag_prompt_builder import build_rag_prompt
from app.services.retrieval_context_builder import build_retrieval_context


router = APIRouter(prefix="/chat", tags=["Chat"])


@router.post("", response_model=ChatResponse)
def create_chat_response(request: ChatRequest) -> ChatResponse:
    context = build_retrieval_context(request.message)
    prompt = build_rag_prompt(
        user_message=request.message,
        context=context,
    )

    try:
        answer = generate_chat_completion(prompt)
        response_message = "Chat response generated with RAG"
    except ValueError:
        answer = (
            "OpenAI API key yapılandırılmadığı için RAG cevabı üretilemedi. "
            "Lütfen yerel .env dosyasına OPENAI_API_KEY değerini ekleyin."
        )
        response_message = "OpenAI API key is not configured"
    except RuntimeError:
        answer = (
            "RAG cevabı üretilirken bir servis hatası oluştu. "
            "Lütfen daha sonra tekrar deneyin."
        )
        response_message = "RAG response generation failed"

    return ChatResponse(
        success=True,
        message=response_message,
        data=ChatResponseData(answer=answer),
    )