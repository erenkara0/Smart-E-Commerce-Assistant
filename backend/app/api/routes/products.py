from fastapi import APIRouter, Query

from app.schemas.product import (
    ProductListResponse,
    ProductListResponseData,
    ProductSearchResponse,
    ProductSearchResponseData,
)
from app.services.product_loader import load_products
from app.services.vector_store_service import vector_store_service

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

@router.get("/search", response_model=ProductSearchResponse)
def search_products(
    query: str = Query(..., min_length=1, max_length=200),
    limit: int = Query(5, ge=1, le=10),
) -> ProductSearchResponse:
    results = vector_store_service.search(query=query, limit=limit)

    return ProductSearchResponse(
        success=True,
        message="Product search completed successfully",
        data=ProductSearchResponseData(
            query=query,    
            results=results,
            total=len(results),
        ),
    )