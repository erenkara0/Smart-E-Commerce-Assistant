from collections.abc import Generator, Sequence
from decimal import Decimal
from pathlib import Path
from typing import Any

import pytest
from openpyxl import Workbook
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.db.base import Base
from app.db.session import create_database_engine
from app.models import ProductModel
from app.services.product_excel_import_service import (
    import_product_excel,
)
from app.services.product_excel_parser import (
    EXPECTED_COLUMNS,
)


def build_product_row(
    **overrides: Any,
) -> dict[str, Any]:
    product: dict[str, Any] = {
        "product_id": "prd-001",
        "sku": "TEST-SKU-001",
        "name": "Test Gaming Laptop",
        "category": "Laptop",
        "brand": "Test Brand",
        "price": 32999.99,
        "currency": "TRY",
        "description": "Test product description.",
        "features": (
            "16 GB RAM | 1 TB SSD | RTX 4060"
        ),
        "stock": 10,
        "rating": 4.5,
        "image_url": (
            "https://example.com/images/prd-001.jpg"
        ),
        "product_url": (
            "https://example.com/products/prd-001"
        ),
        "is_active": "TRUE",
    }

    product.update(overrides)

    return product


def create_product_workbook(
    path: Path,
    rows: Sequence[dict[str, Any]],
) -> None:
    workbook = Workbook()
    worksheet = workbook.active
    worksheet.title = "Products"

    worksheet.append(list(EXPECTED_COLUMNS))

    for product in rows:
        worksheet.append(
            [
                product.get(column_name)
                for column_name in EXPECTED_COLUMNS
            ]
        )

    workbook.save(path)
    workbook.close()


@pytest.fixture()
def db_session(
    tmp_path: Path,
) -> Generator[Session, None, None]:
    database_path = tmp_path / "excel_import.db"
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


def test_valid_excel_creates_products(
    db_session: Session,
    tmp_path: Path,
) -> None:
    excel_path = tmp_path / "valid_products.xlsx"

    first_product = build_product_row()

    second_product = build_product_row(
        product_id="prd-002",
        sku="TEST-SKU-002",
        name="Test Monitor",
        category="Monitor",
        brand="Test Display",
        price=8999.90,
        features="27 inch | QHD | 165 Hz",
        stock=5,
        rating=4.2,
        image_url="",
        product_url="",
        is_active="FALSE",
    )

    create_product_workbook(
        excel_path,
        [
            first_product,
            second_product,
        ],
    )

    result = import_product_excel(
        db_session,
        excel_path,
    )

    assert result.total_rows == 2
    assert result.valid_rows == 2
    assert result.invalid_rows == 0
    assert result.created == 2
    assert result.updated == 0
    assert result.unchanged == 0
    assert result.failed == 0
    assert result.validation_errors == []
    assert result.persistence_errors == []

    stored_products = db_session.scalars(
        select(ProductModel).order_by(
            ProductModel.product_id
        )
    ).all()

    assert len(stored_products) == 2
    assert stored_products[0].price == Decimal(
        "32999.99"
    )
    assert stored_products[0].features == [
        "16 GB RAM",
        "1 TB SSD",
        "RTX 4060",
    ]
    assert stored_products[1].is_active is False
    assert stored_products[1].image_url is None


def test_invalid_excel_does_not_modify_database(
    db_session: Session,
    tmp_path: Path,
) -> None:
    excel_path = tmp_path / "invalid_products.xlsx"

    valid_product = build_product_row()

    invalid_product = build_product_row(
        product_id="prd-002",
        sku="TEST-SKU-002",
        price=0,
        stock=-1,
        rating=6,
    )

    create_product_workbook(
        excel_path,
        [
            valid_product,
            invalid_product,
        ],
    )

    result = import_product_excel(
        db_session,
        excel_path,
    )

    assert result.total_rows == 2
    assert result.valid_rows == 1
    assert result.invalid_rows == 1
    assert result.created == 0
    assert result.updated == 0
    assert result.unchanged == 0
    assert result.failed == 0
    assert result.validation_errors
    assert result.persistence_errors == []

    error_fields = {
        error.field
        for error in result.validation_errors
    }

    assert {
        "price",
        "stock",
        "rating",
    }.issubset(error_fields)

    assert get_product_count(db_session) == 0


def test_reimporting_same_excel_returns_unchanged(
    db_session: Session,
    tmp_path: Path,
) -> None:
    excel_path = tmp_path / "unchanged_products.xlsx"

    create_product_workbook(
        excel_path,
        [build_product_row()],
    )

    first_result = import_product_excel(
        db_session,
        excel_path,
    )
    second_result = import_product_excel(
        db_session,
        excel_path,
    )

    assert first_result.created == 1

    assert second_result.total_rows == 1
    assert second_result.valid_rows == 1
    assert second_result.created == 0
    assert second_result.updated == 0
    assert second_result.unchanged == 1
    assert second_result.failed == 0

    assert get_product_count(db_session) == 1


def test_updated_excel_updates_existing_product(
    db_session: Session,
    tmp_path: Path,
) -> None:
    initial_excel_path = (
        tmp_path / "initial_product.xlsx"
    )
    updated_excel_path = (
        tmp_path / "updated_product.xlsx"
    )

    create_product_workbook(
        initial_excel_path,
        [build_product_row()],
    )

    initial_result = import_product_excel(
        db_session,
        initial_excel_path,
    )

    assert initial_result.created == 1

    stored_product = db_session.scalar(
        select(ProductModel).where(
            ProductModel.product_id == "prd-001"
        )
    )

    assert stored_product is not None

    original_database_id = stored_product.id
    original_created_at = stored_product.created_at

    create_product_workbook(
        updated_excel_path,
        [
            build_product_row(
                name="Updated Gaming Laptop",
                price=31999.50,
                features=(
                    "32 GB RAM | 1 TB SSD | RTX 4070"
                ),
                stock=4,
                rating=4.8,
                is_active="FALSE",
            )
        ],
    )

    update_result = import_product_excel(
        db_session,
        updated_excel_path,
    )

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
    assert refreshed_product.name == (
        "Updated Gaming Laptop"
    )
    assert refreshed_product.price == Decimal(
        "31999.50"
    )
    assert refreshed_product.stock == 4
    assert refreshed_product.rating == Decimal(
        "4.80"
    )
    assert refreshed_product.features == [
        "32 GB RAM",
        "1 TB SSD",
        "RTX 4070",
    ]
    assert refreshed_product.is_active is False
    assert get_product_count(db_session) == 1


def test_sku_conflict_does_not_create_partial_records(
    db_session: Session,
    tmp_path: Path,
) -> None:
    initial_excel_path = (
        tmp_path / "existing_product.xlsx"
    )
    conflicting_excel_path = (
        tmp_path / "conflicting_products.xlsx"
    )

    create_product_workbook(
        initial_excel_path,
        [build_product_row()],
    )

    initial_result = import_product_excel(
        db_session,
        initial_excel_path,
    )

    assert initial_result.created == 1

    valid_new_product = build_product_row(
        product_id="prd-002",
        sku="TEST-SKU-002",
        name="Valid New Product",
    )

    conflicting_product = build_product_row(
        product_id="prd-003",
        sku="TEST-SKU-001",
        name="Conflicting Product",
    )

    create_product_workbook(
        conflicting_excel_path,
        [
            valid_new_product,
            conflicting_product,
        ],
    )

    result = import_product_excel(
        db_session,
        conflicting_excel_path,
    )

    assert result.total_rows == 2
    assert result.valid_rows == 2
    assert result.invalid_rows == 0
    assert result.created == 0
    assert result.updated == 0
    assert result.unchanged == 0
    assert result.failed == 1
    assert result.validation_errors == []
    assert len(result.persistence_errors) == 1

    persistence_error = result.persistence_errors[0]

    assert persistence_error.product_id == "prd-003"
    assert persistence_error.sku == "TEST-SKU-001"
    assert "prd-001" in persistence_error.message

    assert get_product_count(db_session) == 1

    partially_created_product = db_session.scalar(
        select(ProductModel).where(
            ProductModel.product_id == "prd-002"
        )
    )

    assert partially_created_product is None