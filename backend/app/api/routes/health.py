from fastapi import APIRouter
from app.schemas.response import APIResponse

router = APIRouter(tags=["Health"])

@router.get("/health", response_model=APIResponse)
def health_check() -> APIResponse:
    return APIResponse(
        success=True,
        message="API is healthy",
        data={"status": "ok"},
    )