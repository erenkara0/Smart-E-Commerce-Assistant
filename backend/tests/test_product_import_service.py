from collections.abc import Generator
from decimal import Decimal
from pathlib import Path
from typing import Any

import pytest
from sqlalchemy import func, select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.db.base import Base
from app.db.session import create_database_engine
from app.models import ProductModel
from app.schemas.product_import import ExcelProductRow
from app.services.product_import_service import (
    ProductImportServiceError,
    import_products,
)


def build_excel_product(
    **overrides: Any,
) -> ExcelProductRow:
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

    return ExcelProductRow.model_validate(product_data)


@pytest.fixture()
def db_session(
    tmp_path: Path,
) -> Generator[Session, None, None]:
    database_path = tmp_path / "product_import.db"
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


def get_product_count(
    session: Session,
) -> int:
    return session.scalar(
        select(func.count()).select_from(ProductModel)
    ) or 0


def test_empty_import_returns_zero_counts(
    db_session: Session,
) -> None:
    result = import_products(
        db_session,
        [],
    )

    assert result.total_products == 0
    assert result.created == 0
    assert result.updated == 0
    assert result.unchanged == 0
    assert result.failed == 0
    assert result.errors == []
    assert get_product_count(db_session) == 0


def test_new_products_are_created(
    db_session: Session,
) -> None:
    first_product = build_excel_product()

    second_product = build_excel_product(
        product_id="prd-002",
        sku="TEST-SKU-002",
        name="Test Monitor",
        category="Monitor",
        brand="Test Display",
        price=Decimal("8999.90"),
        features=[
            "27 inch",
            "QHD",
            "165 Hz",
        ],
        stock=5,
        rating=Decimal("4.20"),
        image_url=None,
        product_url=None,
        is_active=False,
    )

    result = import_products(
        db_session,
        [
            first_product,
            second_product,
        ],
    )

    assert result.total_products == 2
    assert result.created == 2
    assert result.updated == 0
    assert result.unchanged == 0
    assert result.failed == 0
    assert result.errors == []

    stored_products = db_session.scalars(
        select(ProductModel).order_by(
            ProductModel.product_id
        )
    ).all()

    assert len(stored_products) == 2

    stored_first_product = stored_products[0]

    assert stored_first_product.product_id == "prd-001"
    assert stored_first_product.price == Decimal("32999.99")
    assert stored_first_product.rating == Decimal("4.50")
    assert stored_first_product.features == [
        "16 GB RAM",
        "1 TB SSD",
        "RTX 4060",
    ]
    assert stored_first_product.is_active is True

    stored_second_product = stored_products[1]

    assert stored_second_product.stock == 5
    assert stored_second_product.is_active is False
    assert stored_second_product.image_url is None
    assert stored_second_product.product_url is None


def test_existing_product_is_updated_without_duplication(
    db_session: Session,
) -> None:
    initial_product = build_excel_product()

    first_result = import_products(
        db_session,
        [initial_product],
    )

    assert first_result.created == 1

    stored_product = db_session.scalar(
        select(ProductModel).where(
            ProductModel.product_id == "prd-001"
        )
    )

    assert stored_product is not None

    original_database_id = stored_product.id
    original_created_at = stored_product.created_at

    updated_product = build_excel_product(
        name="Updated Gaming Laptop",
        price=Decimal("31999.50"),
        stock=4,
        rating=Decimal("4.80"),
        features=[
            "32 GB RAM",
            "1 TB SSD",
            "RTX 4070",
        ],
        image_url=None,
        is_active=False,
    )

    update_result = import_products(
        db_session,
        [updated_product],
    )

    assert update_result.total_products == 1
    assert update_result.created == 0
    assert update_result.updated == 1
    assert update_result.unchanged == 0
    assert update_result.failed == 0

    db_session.expire_all()

    refreshed_product = db_session.scalar(
        select(ProductModel).where(
            ProductModel.product_id == "prd-001"
        )
    )

    assert refreshed_product is not None
    assert refreshed_product.id == original_database_id
    assert refreshed_product.created_at == original_created_at
    assert refreshed_product.name == "Updated Gaming Laptop"
    assert refreshed_product.price == Decimal("31999.50")
    assert refreshed_product.stock == 4
    assert refreshed_product.rating == Decimal("4.80")
    assert refreshed_product.features == [
        "32 GB RAM",
        "1 TB SSD",
        "RTX 4070",
    ]
    assert refreshed_product.image_url is None
    assert refreshed_product.is_active is False
    assert get_product_count(db_session) == 1


def test_unchanged_product_is_not_updated(
    db_session: Session,
) -> None:
    product = build_excel_product()

    first_result = import_products(
        db_session,
        [product],
    )
    second_result = import_products(
        db_session,
        [product],
    )

    assert first_result.created == 1

    assert second_result.total_products == 1
    assert second_result.created == 0
    assert second_result.updated == 0
    assert second_result.unchanged == 1
    assert second_result.failed == 0
    assert second_result.errors == []

    assert get_product_count(db_session) == 1


def test_existing_sku_conflict_prevents_complete_import(
    db_session: Session,
) -> None:
    existing_product = build_excel_product()

    import_products(
        db_session,
        [existing_product],
    )

    valid_new_product = build_excel_product(
        product_id="prd-002",
        sku="TEST-SKU-002",
        name="Valid New Product",
    )

    conflicting_product = build_excel_product(
        product_id="prd-003",
        sku="TEST-SKU-001",
        name="Conflicting Product",
    )

    result = import_products(
        db_session,
        [
            valid_new_product,
            conflicting_product,
        ],
    )

    assert result.total_products == 2
    assert result.created == 0
    assert result.updated == 0
    assert result.unchanged == 0
    assert result.failed == 1
    assert len(result.errors) == 1

    conflict_error = result.errors[0]

    assert conflict_error.product_id == "prd-003"
    assert conflict_error.sku == "TEST-SKU-001"
    assert "prd-001" in conflict_error.message

    assert get_product_count(db_session) == 1

    missing_product = db_session.scalar(
        select(ProductModel).where(
            ProductModel.product_id == "prd-002"
        )
    )

    assert missing_product is None


def test_duplicate_product_id_in_batch_is_reported(
    db_session: Session,
) -> None:
    first_product = build_excel_product()

    duplicate_product = build_excel_product(
        sku="TEST-SKU-002",
        name="Duplicate Product ID",
    )

    result = import_products(
        db_session,
        [
            first_product,
            duplicate_product,
        ],
    )

    assert result.total_products == 2
    assert result.created == 0
    assert result.failed == 1
    assert len(result.errors) == 1

    assert result.errors[0].product_id == "prd-001"
    assert "duplicate product_id" in (
        result.errors[0].message.lower()
    )

    assert get_product_count(db_session) == 0


def test_duplicate_sku_in_batch_is_reported(
    db_session: Session,
) -> None:
    first_product = build_excel_product()

    duplicate_sku_product = build_excel_product(
        product_id="prd-002",
        name="Duplicate SKU Product",
    )

    result = import_products(
        db_session,
        [
            first_product,
            duplicate_sku_product,
        ],
    )

    assert result.total_products == 2
    assert result.created == 0
    assert result.failed == 1
    assert len(result.errors) == 1

    assert result.errors[0].product_id == "prd-002"
    assert result.errors[0].sku == "TEST-SKU-001"
    assert "sku" in result.errors[0].message.lower()

    assert get_product_count(db_session) == 0


def test_database_error_rolls_back_complete_import(
    db_session: Session,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    first_product = build_excel_product()

    second_product = build_excel_product(
        product_id="prd-002",
        sku="TEST-SKU-002",
        name="Second Product",
    )

    original_commit = db_session.commit

    def raise_database_error() -> None:
        raise SQLAlchemyError(
            "Simulated database failure."
        )

    monkeypatch.setattr(
        db_session,
        "commit",
        raise_database_error,
    )

    with pytest.raises(
        ProductImportServiceError,
    ) as error_info:
        import_products(
            db_session,
            [
                first_product,
                second_product,
            ],
        )

    assert (
        error_info.value.code
        == "product_import_database_error"
    )

    monkeypatch.setattr(
        db_session,
        "commit",
        original_commit,
    )

    assert get_product_count(db_session) == 0