from collections.abc import Generator
from decimal import Decimal
from pathlib import Path

import pytest
from sqlalchemy.orm import Session

from app.db.base import Base
from app.db.session import create_database_engine
from app.models import ProductModel
from app.repositories.product_repository import (
    list_active_products,
)
from app.services.product_query_service import (
    get_active_products,
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
        description="Database product listing test product.",
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
    database_path = tmp_path / "product_query.db"
    database_url = (
        f"sqlite+pysqlite:///{database_path.as_posix()}"
    )

    engine = create_database_engine(database_url)
    Base.metadata.create_all(engine)

    with Session(
        bind=engine,
        expire_on_commit=False,
    ) as session:
        yield session

    Base.metadata.drop_all(engine)
    engine.dispose()


def test_repository_returns_empty_list(
    db_session: Session,
) -> None:
    products = list_active_products(db_session)

    assert products == []


def test_repository_returns_only_active_products_in_order(
    db_session: Session,
) -> None:
    db_session.add_all(
        [
            build_product_model(
                product_id="prd-003",
                sku="SKU-003",
                name="Third Product",
            ),
            build_product_model(
                product_id="prd-001",
                sku="SKU-001",
                name="First Product",
            ),
            build_product_model(
                product_id="prd-002",
                sku="SKU-002",
                name="Inactive Product",
                is_active=False,
            ),
        ]
    )
    db_session.commit()

    products = list_active_products(db_session)

    assert [
        product.product_id
        for product in products
    ] == [
        "prd-001",
        "prd-003",
    ]


def test_query_service_maps_database_model_to_api_schema(
    db_session: Session,
) -> None:
    db_session.add(
        build_product_model(
            product_id="prd-001",
            sku="SKU-001",
            name="Mapped Product",
        )
    )
    db_session.commit()

    products = get_active_products(db_session)

    assert len(products) == 1

    product = products[0]

    assert product.id == "prd-001"
    assert product.name == "Mapped Product"
    assert product.category == "Laptop"
    assert product.brand == "Test Brand"
    assert product.price == 24999.99
    assert product.currency == "TRY"
    assert product.features == [
        "16 GB RAM",
        "512 GB SSD",
    ]
    assert product.stock == 10
    assert product.rating == 4.5