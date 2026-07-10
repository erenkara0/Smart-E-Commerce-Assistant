from fastapi import APIRouter

from app.schemas.product import ProductListResponse, ProductListResponseData
from app.services.product_loader import load_products


router = APIRouter(prefix="/products", tags=["Products"])


@router.get("", response_model=ProductListResponse)
def list_products() -> ProductListResponse:
    products = load_products()

    return ProductListResponse(
        success=True,
        message="Products listed successfully",
        data=ProductListResponseData(
            products=products,
            total=len(products),
        ),
    )