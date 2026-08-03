from pathlib import Path
from typing import BinaryIO

from sqlalchemy.orm import Session

from app.schemas.product_import import (
    ProductExcelImportResult,
)
from app.services.product_excel_parser import (
    parse_product_excel,
)
from app.services.product_import_service import (
    import_products,
)


def import_product_excel(
    session: Session,
    source: str | Path | BinaryIO,
) -> ProductExcelImportResult:
    """
    Parse, validate, and persist products from an Excel workbook.

    The database is not modified when the workbook contains
    row-level validation errors.
    """

    parse_result = parse_product_excel(source)

    if parse_result.errors:
        return ProductExcelImportResult(
            total_rows=parse_result.total_rows,
            valid_rows=parse_result.valid_rows,
            invalid_rows=parse_result.failed_rows,
            created=0,
            updated=0,
            unchanged=0,
            failed=0,
            validation_errors=parse_result.errors,
            persistence_errors=[],
        )

    persistence_result = import_products(
        session,
        parse_result.products,
    )

    return ProductExcelImportResult(
        total_rows=parse_result.total_rows,
        valid_rows=parse_result.valid_rows,
        invalid_rows=parse_result.failed_rows,
        created=persistence_result.created,
        updated=persistence_result.updated,
        unchanged=persistence_result.unchanged,
        failed=persistence_result.failed,
        validation_errors=[],
        persistence_errors=persistence_result.errors,
    )