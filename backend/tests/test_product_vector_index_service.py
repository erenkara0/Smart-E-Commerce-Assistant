from collections.abc import Generator
from decimal import Decimal
from pathlib import Path

import pytest
from sqlalchemy.orm import Session

from app.db.base import Base
from app.db.session import create_database_engine
from app.models import ProductModel
from app.services.product_vector_index_service import (
    refresh_product_vector_index,
    search_database_products,
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
        price=Decimal("24999.99"),
        currency="TRY",
        description=(
            "Database-backed vector search test product."
        ),
        features=[
            "16 GB RAM",
            "512 GB SSD",
        ],
        stock=10,
        rating=Decimal("4.50"),
        image_url=None,
        product_url=None,
        is_active=is_active,
    )


@pytest.fixture()
def db_session(
    tmp_path: Path,
) -> Generator[Session, None, None]:
    database_path = (
        tmp_path / "product_vector_index.db"
    )
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


def test_empty_database_creates_empty_index(
    db_session: Session,
) -> None:
    vector_store_service.build_index(
        ["Stale product document"]
    )

    documents = refresh_product_vector_index(
        db_session
    )

    assert documents == []
    assert vector_store_service.get_documents() == []


def test_refresh_indexes_only_active_products_in_order(
    db_session: Session,
) -> None:
    db_session.add_all(
        [
            build_product_model(
                product_id="prd-003",
                sku="SKU-003",
                name="Third Active Laptop",
            ),
            build_product_model(
                product_id="prd-001",
                sku="SKU-001",
                name="First Active Laptop",
            ),
            build_product_model(
                product_id="prd-002",
                sku="SKU-002",
                name="Inactive Laptop",
                is_active=False,
            ),
        ]
    )
    db_session.commit()

    documents = refresh_product_vector_index(
        db_session
    )

    assert len(documents) == 2
    assert "prd-001" in documents[0]
    assert "First Active Laptop" in documents[0]
    assert "prd-003" in documents[1]
    assert "Third Active Laptop" in documents[1]

    combined_documents = "\n".join(documents)

    assert "Inactive Laptop" not in combined_documents
    assert "prd-002" not in combined_documents


def test_rebuilding_index_does_not_duplicate_documents(
    db_session: Session,
) -> None:
    db_session.add(
        build_product_model(
            product_id="prd-001",
            sku="SKU-001",
            name="Reusable Index Laptop",
        )
    )
    db_session.commit()

    first_documents = refresh_product_vector_index(
        db_session
    )
    second_documents = refresh_product_vector_index(
        db_session
    )

    assert len(first_documents) == 1
    assert len(second_documents) == 1
    assert first_documents == second_documents
    assert len(
        vector_store_service.get_documents()
    ) == 1


def test_search_returns_matching_active_product(
    db_session: Session,
) -> None:
    db_session.add_all(
        [
            build_product_model(
                product_id="prd-001",
                sku="SKU-001",
                name="Falcon Gaming Laptop",
            ),
            build_product_model(
                product_id="prd-002",
                sku="SKU-002",
                name="Office Notebook",
            ),
            build_product_model(
                product_id="prd-003",
                sku="SKU-003",
                name="Falcon Inactive Laptop",
                is_active=False,
            ),
        ]
    )
    db_session.commit()

    results = search_database_products(
        session=db_session,
        query="Falcon",
        limit=5,
    )

    assert len(results) == 1
    assert "Falcon Gaming Laptop" in str(
        results[0]["document"]
    )
    assert "Falcon Inactive Laptop" not in str(
        results[0]["document"]
    )
    assert int(results[0]["score"]) > 0