from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.db.session import get_database_session
from app.schemas.product import (
    ProductListResponse,
    ProductListResponseData,
    ProductSearchResponse,
    ProductSearchResponseData,
)
from app.services.product_query_service import (
    get_active_products,
)
from app.services.product_vector_index_service import (
    search_database_products,
)


router = APIRouter(
    prefix="/products",
    tags=["Products"],
)


@router.get(
    "",
    response_model=ProductListResponse,
)
def list_products(
    session: Annotated[
        Session,
        Depends(get_database_session),
    ],
) -> ProductListResponse:
    products = get_active_products(session)

    return ProductListResponse(
        success=True,
        message="Products listed successfully",
        data=ProductListResponseData(
            products=products,
            total=len(products),
        ),
    )


@router.get(
    "/search",
    response_model=ProductSearchResponse,
)
def search_products(
    session: Annotated[
        Session,
        Depends(get_database_session),
    ],
    query: str = Query(
        ...,
        min_length=1,
        max_length=200,
    ),
    limit: int = Query(
        5,
        ge=1,
        le=10,
    ),
) -> ProductSearchResponse:
    results = search_database_products(
        session=session,
        query=query,
        limit=limit,
    )

    return ProductSearchResponse(
        success=True,
        message="Product search completed successfully",
        data=ProductSearchResponseData(
            query=query,
            results=results,
            total=len(results),
        ),
    )