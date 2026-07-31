from pathlib import Path
from typing import Any, Sequence

import pytest
from openpyxl import Workbook

from app.services.product_excel_parser import (
    EXPECTED_COLUMNS,
    ProductExcelParserError,
    parse_product_excel,
)


def build_valid_product(
    **overrides: Any,
) -> dict[str, Any]:
    product: dict[str, Any] = {
        "product_id": "prd-100",
        "sku": "TEST-SKU-100",
        "name": "Test Gaming Laptop",
        "category": "Laptop",
        "brand": "Test Brand",
        "price": 34999.99,
        "currency": "TRY",
        "description": "Test ürün açıklaması.",
        "features": (
            "16 GB RAM | 1 TB SSD | RTX 4060"
        ),
        "stock": 10,
        "rating": 4.5,
        "image_url": "",
        "product_url": "",
        "is_active": "TRUE",
    }

    product.update(overrides)

    return product


def create_workbook(
    path: Path,
    *,
    sheet_name: str = "Products",
    headers: Sequence[str] | None = EXPECTED_COLUMNS,
    rows: Sequence[dict[str, Any] | None] = (),
) -> None:
    workbook = Workbook()
    worksheet = workbook.active
    worksheet.title = sheet_name

    if headers is not None:
        worksheet.append(list(headers))

        for row in rows:
            if row is None:
                worksheet.append(
                    [None for _ in headers]
                )
                continue

            worksheet.append(
                [
                    row.get(column_name)
                    for column_name in headers
                ]
            )

    workbook.save(path)
    workbook.close()


def test_parser_returns_normalized_products(
    tmp_path: Path,
) -> None:
    excel_path = tmp_path / "valid_products.xlsx"

    first_product = build_valid_product(
        product_id="  prd-101  ",
        sku="  TEST-SKU-101  ",
        currency=" try ",
        features=(
            "16 GB RAM | RTX 4060 | "
            "16 GB RAM | 1 TB SSD"
        ),
        image_url="",
        product_url="",
        is_active="TRUE",
    )
    second_product = build_valid_product(
        product_id="prd-102",
        sku="TEST-SKU-102",
        name="Test Monitor",
        category="Monitor",
        brand="Test Display",
        price=8999.90,
        features="27 inç | QHD | 165 Hz",
        stock=0,
        rating=4.2,
        is_active=False,
    )

    create_workbook(
        excel_path,
        rows=[
            first_product,
            None,
            second_product,
        ],
    )

    result = parse_product_excel(excel_path)

    assert result.total_rows == 2
    assert result.valid_rows == 2
    assert result.failed_rows == 0
    assert result.errors == []

    parsed_first_product = result.products[0]

    assert parsed_first_product.product_id == "prd-101"
    assert parsed_first_product.sku == "TEST-SKU-101"
    assert parsed_first_product.currency == "TRY"
    assert parsed_first_product.features == [
        "16 GB RAM",
        "RTX 4060",
        "1 TB SSD",
    ]
    assert parsed_first_product.image_url is None
    assert parsed_first_product.product_url is None
    assert parsed_first_product.is_active is True

    parsed_second_product = result.products[1]

    assert parsed_second_product.stock == 0
    assert parsed_second_product.is_active is False


def test_parser_rejects_missing_products_worksheet(
    tmp_path: Path,
) -> None:
    excel_path = tmp_path / "missing_products_sheet.xlsx"

    create_workbook(
        excel_path,
        sheet_name="Inventory",
        rows=[build_valid_product()],
    )

    with pytest.raises(
        ProductExcelParserError,
    ) as error_info:
        parse_product_excel(excel_path)

    assert (
        error_info.value.code
        == "missing_products_worksheet"
    )
    assert "Products" in str(error_info.value)


def test_parser_rejects_missing_header_row(
    tmp_path: Path,
) -> None:
    excel_path = tmp_path / "missing_headers.xlsx"

    create_workbook(
        excel_path,
        headers=None,
    )

    with pytest.raises(
        ProductExcelParserError,
    ) as error_info:
        parse_product_excel(excel_path)

    assert error_info.value.code == "missing_header_row"


def test_parser_reports_missing_required_columns(
    tmp_path: Path,
) -> None:
    excel_path = tmp_path / "missing_columns.xlsx"

    headers = [
        column_name
        for column_name in EXPECTED_COLUMNS
        if column_name != "stock"
    ]

    create_workbook(
        excel_path,
        headers=headers,
    )

    with pytest.raises(
        ProductExcelParserError,
    ) as error_info:
        parse_product_excel(excel_path)

    assert error_info.value.code == "missing_columns"
    assert "stock" in str(error_info.value)


def test_parser_rejects_duplicate_columns(
    tmp_path: Path,
) -> None:
    excel_path = tmp_path / "duplicate_columns.xlsx"

    headers = list(EXPECTED_COLUMNS)
    headers[-1] = "product_id"

    create_workbook(
        excel_path,
        headers=headers,
    )

    with pytest.raises(
        ProductExcelParserError,
    ) as error_info:
        parse_product_excel(excel_path)

    assert error_info.value.code == "duplicate_columns"
    assert "product_id" in str(error_info.value)


def test_parser_returns_structured_row_errors(
    tmp_path: Path,
) -> None:
    excel_path = tmp_path / "invalid_product.xlsx"

    invalid_product = build_valid_product(
        price=0,
        currency="GBP",
        features="",
        stock=-1,
        rating=6,
        image_url="invalid-image-url",
        is_active="yes",
    )

    create_workbook(
        excel_path,
        rows=[invalid_product],
    )

    result = parse_product_excel(excel_path)

    assert result.total_rows == 1
    assert result.valid_rows == 0
    assert result.failed_rows == 1
    assert result.products == []

    error_fields = {
        error.field
        for error in result.errors
    }

    assert {
        "price",
        "currency",
        "features",
        "stock",
        "rating",
        "image_url",
        "is_active",
    }.issubset(error_fields)

    assert all(
        error.row == 2
        for error in result.errors
    )
    assert all(
        error.message
        for error in result.errors
    )


def test_parser_detects_duplicate_product_id_and_sku(
    tmp_path: Path,
) -> None:
    excel_path = tmp_path / "duplicate_products.xlsx"

    first_product = build_valid_product(
        product_id="prd-duplicate",
        sku="SKU-DUPLICATE",
    )
    duplicate_product = build_valid_product(
        product_id="prd-duplicate",
        sku="SKU-DUPLICATE",
        name="Duplicate Product",
    )

    create_workbook(
        excel_path,
        rows=[
            first_product,
            duplicate_product,
        ],
    )

    result = parse_product_excel(excel_path)

    assert result.total_rows == 2
    assert result.valid_rows == 1
    assert result.failed_rows == 1

    duplicate_errors = [
        error
        for error in result.errors
        if error.row == 3
    ]

    assert {
        error.field
        for error in duplicate_errors
    } == {
        "product_id",
        "sku",
    }

    assert all(
        "row 2" in error.message
        for error in duplicate_errors
    )


def test_parser_rejects_invalid_xlsx_file(
    tmp_path: Path,
) -> None:
    excel_path = tmp_path / "invalid_file.xlsx"
    excel_path.write_text(
        "This is not an Excel workbook.",
        encoding="utf-8",
    )

    with pytest.raises(
        ProductExcelParserError,
    ) as error_info:
        parse_product_excel(excel_path)

    assert error_info.value.code == "invalid_excel_file"