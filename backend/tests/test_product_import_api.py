from collections.abc import Generator, Sequence
from io import BytesIO
from pathlib import Path
from typing import Any

import pytest
from fastapi.testclient import TestClient
from openpyxl import Workbook
from sqlalchemy import Engine, func, select
from sqlalchemy.orm import Session

from app.db.base import Base
from app.db.session import (
    create_database_engine,
    get_database_session,
)
from app.main import app
from app.models import ProductModel
from app.services.product_excel_parser import (
    EXPECTED_COLUMNS,
)


EXCEL_CONTENT_TYPE = (
    "application/vnd.openxmlformats-officedocument."
    "spreadsheetml.sheet"
)


def build_product_row(
    **overrides: Any,
) -> dict[str, Any]:
    product: dict[str, Any] = {
        "product_id": "prd-api-001",
        "sku": "API-SKU-001",
        "name": "API Test Laptop",
        "category": "Laptop",
        "brand": "Test Brand",
        "price": 29999.99,
        "currency": "TRY",
        "description": "Product used in API endpoint tests.",
        "features": "16 GB RAM | 1 TB SSD | RTX 4060",
        "stock": 8,
        "rating": 4.5,
        "image_url": (
            "https://example.com/images/prd-api-001.jpg"
        ),
        "product_url": (
            "https://example.com/products/prd-api-001"
        ),
        "is_active": "TRUE",
    }

    product.update(overrides)

    return product


def create_product_workbook(
    rows: Sequence[dict[str, Any]],
) -> bytes:
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

    workbook_stream = BytesIO()
    workbook.save(workbook_stream)
    workbook.close()

    return workbook_stream.getvalue()


@pytest.fixture()
def import_api_database(
    tmp_path: Path,
) -> Generator[Engine, None, None]:
    database_path = tmp_path / "product_import_api.db"
    database_url = (
        f"sqlite+pysqlite:///{database_path.as_posix()}"
    )

    engine = create_database_engine(database_url)
    Base.metadata.create_all(engine)

    def override_get_database_session(
    ) -> Generator[Session, None, None]:
        with Session(
            bind=engine,
            expire_on_commit=False,
        ) as session:
            yield session

    app.dependency_overrides[
        get_database_session
    ] = override_get_database_session

    try:
        yield engine
    finally:
        app.dependency_overrides.pop(
            get_database_session,
            None,
        )
        Base.metadata.drop_all(engine)
        engine.dispose()


def get_product_count(
    engine: Engine,
) -> int:
    with Session(bind=engine) as session:
        return session.scalar(
            select(func.count()).select_from(
                ProductModel
            )
        ) or 0


def test_valid_excel_upload_creates_product(
    client: TestClient,
    import_api_database: Engine,
) -> None:
    workbook_content = create_product_workbook(
        [build_product_row()]
    )

    response = client.post(
        "/products/import/excel",
        files={
            "file": (
                "products.xlsx",
                workbook_content,
                EXCEL_CONTENT_TYPE,
            )
        },
    )

    assert response.status_code == 200

    response_body = response.json()
    result = response_body["data"]

    assert response_body["success"] is True
    assert response_body["message"] == (
        "Product Excel import completed successfully"
    )
    assert result["total_rows"] == 1
    assert result["valid_rows"] == 1
    assert result["invalid_rows"] == 0
    assert result["created"] == 1
    assert result["updated"] == 0
    assert result["unchanged"] == 0
    assert result["failed"] == 0
    assert result["validation_errors"] == []
    assert result["persistence_errors"] == []

    assert get_product_count(import_api_database) == 1


def test_invalid_excel_rows_do_not_modify_database(
    client: TestClient,
    import_api_database: Engine,
) -> None:
    valid_product = build_product_row()

    invalid_product = build_product_row(
        product_id="prd-api-002",
        sku="API-SKU-002",
        price=0,
        stock=-1,
        rating=6,
    )

    workbook_content = create_product_workbook(
        [
            valid_product,
            invalid_product,
        ]
    )

    response = client.post(
        "/products/import/excel",
        files={
            "file": (
                "invalid-products.xlsx",
                workbook_content,
                EXCEL_CONTENT_TYPE,
            )
        },
    )

    assert response.status_code == 200

    response_body = response.json()
    result = response_body["data"]

    assert response_body["success"] is False
    assert response_body["message"] == (
        "Product Excel import completed with errors"
    )
    assert result["total_rows"] == 2
    assert result["valid_rows"] == 1
    assert result["invalid_rows"] == 1
    assert result["created"] == 0
    assert result["validation_errors"]

    assert get_product_count(import_api_database) == 0


def test_unsupported_file_extension_is_rejected(
    client: TestClient,
    import_api_database: Engine,
) -> None:
    response = client.post(
        "/products/import/excel",
        files={
            "file": (
                "products.csv",
                b"product_id,sku,name",
                "text/csv",
            )
        },
    )

    assert response.status_code == 415

    response_body = response.json()

    assert response_body["success"] is False
    assert response_body["message"] == (
        "Only .xlsx Excel files are supported."
    )
    assert response_body["data"] is None


def test_unsupported_content_type_is_rejected(
    client: TestClient,
    import_api_database: Engine,
) -> None:
    workbook_content = create_product_workbook(
        [build_product_row()]
    )

    response = client.post(
        "/products/import/excel",
        files={
            "file": (
                "products.xlsx",
                workbook_content,
                "text/plain",
            )
        },
    )

    assert response.status_code == 415

    response_body = response.json()

    assert response_body["success"] is False
    assert response_body["message"] == (
        "The uploaded file has an unsupported "
        "content type."
    )
    assert response_body["data"] is None


def test_empty_excel_file_is_rejected(
    client: TestClient,
    import_api_database: Engine,
) -> None:
    response = client.post(
        "/products/import/excel",
        files={
            "file": (
                "empty.xlsx",
                b"",
                EXCEL_CONTENT_TYPE,
            )
        },
    )

    assert response.status_code == 400

    response_body = response.json()

    assert response_body["success"] is False
    assert response_body["message"] == (
        "The uploaded Excel file is empty."
    )
    assert response_body["data"] is None


def test_corrupted_excel_file_is_rejected(
    client: TestClient,
    import_api_database: Engine,
) -> None:
    response = client.post(
        "/products/import/excel",
        files={
            "file": (
                "corrupted.xlsx",
                b"This is not an Excel workbook.",
                EXCEL_CONTENT_TYPE,
            )
        },
    )

    assert response.status_code == 422

    response_body = response.json()

    assert response_body["success"] is False
    assert response_body["message"] == (
        "The uploaded file is not a valid .xlsx workbook."
    )
    assert response_body["data"] is None


def test_sku_conflict_does_not_create_partial_records(
    client: TestClient,
    import_api_database: Engine,
) -> None:
    initial_workbook = create_product_workbook(
        [build_product_row()]
    )

    initial_response = client.post(
        "/products/import/excel",
        files={
            "file": (
                "initial-products.xlsx",
                initial_workbook,
                EXCEL_CONTENT_TYPE,
            )
        },
    )

    assert initial_response.status_code == 200
    assert initial_response.json()["data"]["created"] == 1

    valid_new_product = build_product_row(
        product_id="prd-api-002",
        sku="API-SKU-002",
        name="Valid New Product",
    )

    conflicting_product = build_product_row(
        product_id="prd-api-003",
        sku="API-SKU-001",
        name="Conflicting Product",
    )

    conflicting_workbook = create_product_workbook(
        [
            valid_new_product,
            conflicting_product,
        ]
    )

    response = client.post(
        "/products/import/excel",
        files={
            "file": (
                "conflicting-products.xlsx",
                conflicting_workbook,
                EXCEL_CONTENT_TYPE,
            )
        },
    )

    assert response.status_code == 200

    response_body = response.json()
    result = response_body["data"]

    assert response_body["success"] is False
    assert result["created"] == 0
    assert result["updated"] == 0
    assert result["unchanged"] == 0
    assert result["failed"] == 1
    assert len(result["persistence_errors"]) == 1

    persistence_error = result[
        "persistence_errors"
    ][0]

    assert persistence_error["product_id"] == (
        "prd-api-003"
    )
    assert persistence_error["sku"] == "API-SKU-001"

    assert get_product_count(import_api_database) == 1