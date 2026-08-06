from sqlalchemy.orm import Session

from app.services.product_document_builder import (
    build_product_documents,
)
from app.services.product_query_service import (
    get_active_products,
)
from app.services.vector_store_service import (
    vector_store_service,
)


def refresh_product_vector_index(
    session: Session,
) -> list[str]:
    products = get_active_products(session)
    documents = build_product_documents(products)

    return vector_store_service.build_index(documents)


def search_database_products(
    session: Session,
    query: str,
    limit: int = 5,
) -> list[dict[str, str | int]]:
    refresh_product_vector_index(session)

    return vector_store_service.search(
        query=query,
        limit=limit,
    )