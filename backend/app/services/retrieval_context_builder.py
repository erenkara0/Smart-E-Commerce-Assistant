from sqlalchemy.orm import Session

from app.core.config import settings
from app.services.product_vector_index_service import (
    search_database_products,
)


def build_retrieval_context(
    session: Session,
    query: str,
    limit: int | None = None,
) -> str:
    search_limit = limit or settings.retrieval_top_k

    results = search_database_products(
        session=session,
        query=query,
        limit=search_limit,
    )

    if not results:
        return ""

    context_parts: list[str] = []

    for index, result in enumerate(
        results,
        start=1,
    ):
        document = str(result["document"])
        score = int(result["score"])

        context_parts.append(
            f"Kaynak {index}:\n"
            f"Skor: {score}\n"
            f"{document}"
        )

    context = "\n\n---\n\n".join(
        context_parts
    )

    return context[
        : settings.rag_max_context_chars
    ]