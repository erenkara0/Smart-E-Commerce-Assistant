from collections.abc import Generator
from decimal import Decimal
from pathlib import Path
from typing import Any

import pytest
from sqlalchemy import inspect, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.db import session as database_session_module
from app.db.base import Base
from app.db.session import create_database_engine
from app.models import ProductModel


EXPECTED_PRODUCT_COLUMNS = {
    "id",
    "product_id",
    "sku",
    "name",
    "category",
    "brand",
    "price",
    "currency",
    "description",
    "features",
    "stock",
    "rating",
    "image_url",
    "product_url",
    "is_active",
    "created_at",
    "updated_at",
}


def build_product(
    **overrides: Any,
) -> ProductModel:
    product_data: dict[str, Any] = {
        "product_id": "prd-001",
        "sku": "TEST-SKU-001",
        "name": "Test Gaming Laptop",
        "category": "Laptop",
        "brand": "Test Brand",
        "price": Decimal("32999.99"),
        "currency": "TRY",
        "description": "Test product description.",
        "features": [
            "16 GB RAM",
            "1 TB SSD",
            "RTX 4060",
        ],
        "stock": 10,
        "rating": Decimal("4.50"),
        "image_url": "https://example.com/product.jpg",
        "product_url": "https://example.com/product",
        "is_active": True,
    }

    product_data.update(overrides)

    return ProductModel(**product_data)


@pytest.fixture()
def db_session(
    tmp_path: Path,
) -> Generator[Session, None, None]:
    database_path = tmp_path / "products.db"
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

    engine.dispose()


def test_products_table_contains_expected_columns(
    db_session: Session,
) -> None:
    inspector = inspect(db_session.get_bind())

    column_names = {
        column["name"]
        for column in inspector.get_columns("products")
    }

    assert column_names == EXPECTED_PRODUCT_COLUMNS


def test_valid_product_can_be_persisted(
    db_session: Session,
) -> None:
    product = build_product()

    db_session.add(product)
    db_session.commit()
    db_session.refresh(product)

    assert product.id is not None
    assert product.product_id == "prd-001"
    assert product.price == Decimal("32999.99")
    assert product.rating == Decimal("4.50")
    assert product.features == [
        "16 GB RAM",
        "1 TB SSD",
        "RTX 4060",
    ]
    assert product.created_at is not None
    assert product.updated_at is not None


def test_product_id_must_be_unique(
    db_session: Session,
) -> None:
    first_product = build_product()
    duplicate_product = build_product(
        sku="TEST-SKU-002",
    )

    db_session.add(first_product)
    db_session.commit()

    db_session.add(duplicate_product)

    with pytest.raises(IntegrityError):
        db_session.commit()

    db_session.rollback()


def test_sku_must_be_unique(
    db_session: Session,
) -> None:
    first_product = build_product()
    duplicate_product = build_product(
        product_id="prd-002",
    )

    db_session.add(first_product)
    db_session.commit()

    db_session.add(duplicate_product)

    with pytest.raises(IntegrityError):
        db_session.commit()

    db_session.rollback()


@pytest.mark.parametrize(
    ("field_name", "invalid_value"),
    [
        ("price", Decimal("0")),
        ("stock", -1),
        ("rating", Decimal("5.10")),
    ],
)
def test_database_rejects_invalid_numeric_values(
    db_session: Session,
    field_name: str,
    invalid_value: Any,
) -> None:
    product = build_product(
        **{
            field_name: invalid_value,
        }
    )

    db_session.add(product)

    with pytest.raises(IntegrityError):
        db_session.commit()

    db_session.rollback()


def test_active_and_inactive_products_can_be_stored(
    db_session: Session,
) -> None:
    active_product = build_product()

    inactive_product = build_product(
        product_id="prd-002",
        sku="TEST-SKU-002",
        name="Inactive Product",
        is_active=False,
        stock=0,
    )

    db_session.add_all(
        [
            active_product,
            inactive_product,
        ]
    )
    db_session.commit()

    products = db_session.scalars(
        select(ProductModel).order_by(
            ProductModel.product_id
        )
    ).all()

    assert len(products) == 2
    assert products[0].is_active is True
    assert products[1].is_active is False


def test_database_session_dependency_closes_session(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    class FakeSession:
        def __init__(self) -> None:
            self.closed = False

        def close(self) -> None:
            self.closed = True

    fake_session = FakeSession()

    monkeypatch.setattr(
        database_session_module,
        "SessionLocal",
        lambda: fake_session,
    )

    session_dependency = (
        database_session_module.get_database_session()
    )

    yielded_session = next(session_dependency)

    assert yielded_session is fake_session
    assert fake_session.closed is False

    session_dependency.close()

    assert fake_session.closed is True