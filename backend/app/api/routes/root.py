from fastapi import APIRouter

from app.schemas.response import APIResponse

router = APIRouter()


@router.get("/", response_model=APIResponse)
def read_root() -> APIResponse:
    return APIResponse(
        success=True,
        message="MikroAsistan API is running",
        data=None,
    )