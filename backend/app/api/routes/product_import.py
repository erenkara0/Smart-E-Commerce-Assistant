from pathlib import Path
from typing import Annotated

from fastapi import (
    APIRouter,
    Depends,
    File,
    HTTPException,
    UploadFile,
    status,
)
from sqlalchemy.orm import Session

from app.db.session import get_database_session
from app.schemas.product_import import (
    ProductExcelImportResponse,
)
from app.services.product_excel_import_service import (
    import_product_excel,
)
from app.services.product_excel_parser import (
    ProductExcelParserError,
)
from app.services.product_import_service import (
    ProductImportServiceError,
)


router = APIRouter(
    prefix="/products",
    tags=["Products"],
)

ALLOWED_EXCEL_CONTENT_TYPES = {
    (
        "application/vnd.openxmlformats-officedocument."
        "spreadsheetml.sheet"
    ),
    "application/octet-stream",
}


@router.post(
    "/import/excel",
    response_model=ProductExcelImportResponse,
)
async def import_products_from_excel(
    file: Annotated[UploadFile, File(...)],
    session: Annotated[
        Session,
        Depends(get_database_session),
    ],
) -> ProductExcelImportResponse:
    filename = file.filename or ""
    file_extension = Path(filename).suffix.lower()

    if file_extension != ".xlsx":
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail="Only .xlsx Excel files are supported.",
        )

    if file.content_type not in ALLOWED_EXCEL_CONTENT_TYPES:
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail=(
                "The uploaded file has an unsupported "
                "content type."
            ),
        )

    first_byte = await file.read(1)

    if not first_byte:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The uploaded Excel file is empty.",
        )

    await file.seek(0)

    try:
        import_result = import_product_excel(
            session=session,
            source=file.file,
        )
    except ProductExcelParserError as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail=str(exc),
        ) from exc
    except ProductImportServiceError as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(exc),
        ) from exc
    finally:
        await file.close()

    has_errors = bool(
        import_result.validation_errors
        or import_result.persistence_errors
    )

    if has_errors:
        return ProductExcelImportResponse(
            success=False,
            message=(
                "Product Excel import completed with errors"
            ),
            data=import_result,
        )

    return ProductExcelImportResponse(
        success=True,
        message=(
            "Product Excel import completed successfully"
        ),
        data=import_result,
    )