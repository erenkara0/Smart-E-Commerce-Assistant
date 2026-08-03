from collections.abc import Sequence
from typing import Any

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.models import ProductModel
from app.schemas.product_import import (
    ExcelProductRow,
    ProductDatabaseImportResult,
    ProductPersistenceError,
)


UPDATABLE_PRODUCT_FIELDS = (
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
)


class ProductImportServiceError(RuntimeError):
    def __init__(
        self,
        code: str,
        message: str,
    ) -> None:
        super().__init__(message)
        self.code = code


def normalize_optional_url(
    value: object,
) -> str | None:
    if value is None:
        return None

    normalized_value = str(value).strip()

    return normalized_value or None


def build_product_values(
    product: ExcelProductRow,
) -> dict[str, Any]:
    return {
        "product_id": product.product_id,
        "sku": product.sku,
        "name": product.name,
        "category": product.category,
        "brand": product.brand,
        "price": product.price,
        "currency": str(product.currency),
        "description": product.description,
        "features": list(product.features),
        "stock": product.stock,
        "rating": product.rating,
        "image_url": normalize_optional_url(
            product.image_url
        ),
        "product_url": normalize_optional_url(
            product.product_url
        ),
        "is_active": product.is_active,
    }


def product_has_changes(
    stored_product: ProductModel,
    incoming_values: dict[str, Any],
) -> bool:
    return any(
        getattr(stored_product, field_name)
        != incoming_values[field_name]
        for field_name in UPDATABLE_PRODUCT_FIELDS
    )


def update_product(
    stored_product: ProductModel,
    incoming_values: dict[str, Any],
) -> None:
    for field_name in UPDATABLE_PRODUCT_FIELDS:
        setattr(
            stored_product,
            field_name,
            incoming_values[field_name],
        )


def find_batch_conflicts(
    products: Sequence[ExcelProductRow],
    existing_by_product_id: dict[str, ProductModel],
    existing_by_sku: dict[str, ProductModel],
) -> list[ProductPersistenceError]:
    errors: list[ProductPersistenceError] = []
    seen_product_ids: set[str] = set()
    seen_skus: dict[str, str] = {}

    for product in products:
        if product.product_id in seen_product_ids:
            errors.append(
                ProductPersistenceError(
                    product_id=product.product_id,
                    sku=product.sku,
                    message=(
                        "The import batch contains a duplicate "
                        "product_id."
                    ),
                )
            )
            continue

        seen_product_ids.add(product.product_id)

        previous_product_id = seen_skus.get(product.sku)

        if (
            previous_product_id is not None
            and previous_product_id != product.product_id
        ):
            errors.append(
                ProductPersistenceError(
                    product_id=product.product_id,
                    sku=product.sku,
                    message=(
                        "The import batch contains an SKU "
                        "assigned to another product."
                    ),
                )
            )
            continue

        seen_skus[product.sku] = product.product_id

        stored_by_id = existing_by_product_id.get(
            product.product_id
        )
        stored_by_sku = existing_by_sku.get(product.sku)

        if (
            stored_by_sku is not None
            and (
                stored_by_id is None
                or stored_by_sku.id != stored_by_id.id
            )
        ):
            errors.append(
                ProductPersistenceError(
                    product_id=product.product_id,
                    sku=product.sku,
                    message=(
                        "The SKU is already assigned to "
                        f"product_id '{stored_by_sku.product_id}'."
                    ),
                )
            )

    return errors


def import_products(
    session: Session,
    products: Sequence[ExcelProductRow],
) -> ProductDatabaseImportResult:
    normalized_products = list(products)

    if not normalized_products:
        return ProductDatabaseImportResult()

    product_ids = {
        product.product_id
        for product in normalized_products
    }
    skus = {
        product.sku
        for product in normalized_products
    }

    existing_products_by_id = session.scalars(
        select(ProductModel).where(
            ProductModel.product_id.in_(product_ids)
        )
    ).all()

    existing_products_by_sku = session.scalars(
        select(ProductModel).where(
            ProductModel.sku.in_(skus)
        )
    ).all()

    existing_by_product_id = {
        product.product_id: product
        for product in existing_products_by_id
    }
    existing_by_sku = {
        product.sku: product
        for product in existing_products_by_sku
    }

    conflict_errors = find_batch_conflicts(
        normalized_products,
        existing_by_product_id,
        existing_by_sku,
    )

    if conflict_errors:
        session.rollback()

        failed_product_ids = {
            error.product_id
            for error in conflict_errors
            if error.product_id is not None
        }

        return ProductDatabaseImportResult(
            total_products=len(normalized_products),
            failed=len(failed_product_ids),
            errors=conflict_errors,
        )

    created = 0
    updated = 0
    unchanged = 0

    try:
        for product in normalized_products:
            incoming_values = build_product_values(product)
            stored_product = existing_by_product_id.get(
                product.product_id
            )

            if stored_product is None:
                session.add(
                    ProductModel(**incoming_values)
                )
                created += 1
                continue

            if not product_has_changes(
                stored_product,
                incoming_values,
            ):
                unchanged += 1
                continue

            update_product(
                stored_product,
                incoming_values,
            )
            updated += 1

        session.commit()
    except SQLAlchemyError as exc:
        session.rollback()

        raise ProductImportServiceError(
            code="product_import_database_error",
            message=(
                "The product import transaction could not "
                "be completed."
            ),
        ) from exc

    return ProductDatabaseImportResult(
        total_products=len(normalized_products),
        created=created,
        updated=updated,
        unchanged=unchanged,
        failed=0,
    )