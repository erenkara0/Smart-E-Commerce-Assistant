from collections.abc import Generator
from decimal import Decimal
from pathlib import Path

import pytest
from sqlalchemy.orm import Session

from app.db.base import Base
from app.db.session import create_database_engine
from app.models import ProductModel
from app.services.retrieval_context_builder import (
    build_retrieval_context,
)
from app.services.vector_store_service import (
    vector_store_service,
)


def build_product_model(
    product_id: str,
    sku: str,
    name: str,
    *,
    is_active: bool = True,
) -> ProductModel:
    return ProductModel(
        product_id=product_id,
        sku=sku,
        name=name,
        category="Laptop",
        brand="Test Brand",
        price=Decimal("25999.99"),
        currency="TRY",
        description="RAG retrieval context test product.",
        features=[
            "16 GB RAM",
            "1 TB SSD",
        ],
        stock=7,
        rating=Decimal("4.60"),
        image_url=None,
        product_url=None,
        is_active=is_active,
    )


@pytest.fixture()
def db_session(
    tmp_path: Path,
) -> Generator[Session, None, None]:
    database_path = tmp_path / "retrieval_context.db"
    database_url = (
        f"sqlite+pysqlite:///{database_path.as_posix()}"
    )

    engine = create_database_engine(database_url)
    Base.metadata.create_all(engine)
    vector_store_service.clear()

    with Session(
        bind=engine,
        expire_on_commit=False,
    ) as session:
        yield session

    vector_store_service.clear()
    Base.metadata.drop_all(engine)
    engine.dispose()


def test_retrieval_context_uses_active_database_products(
    db_session: Session,
) -> None:
    db_session.add_all(
        [
            build_product_model(
                product_id="prd-rag-001",
                sku="RAG-SKU-001",
                name="Orion Gaming Laptop",
            ),
            build_product_model(
                product_id="prd-rag-002",
                sku="RAG-SKU-002",
                name="Orion Inactive Laptop",
                is_active=False,
            ),
        ]
    )
    db_session.commit()

    context = build_retrieval_context(
        session=db_session,
        query="Orion",
    )

    assert context
    assert "Orion Gaming Laptop" in context
    assert "prd-rag-001" in context

    assert "Orion Inactive Laptop" not in context
    assert "prd-rag-002" not in context


def test_retrieval_context_returns_empty_for_empty_database(
    db_session: Session,
) -> None:
    context = build_retrieval_context(
        session=db_session,
        query="gaming laptop",
    )

    assert context == ""
    assert vector_store_service.get_documents() == []