from sqlalchemy.orm import Session

from app.models import ProductModel
from app.repositories.product_repository import (
    list_active_products,
)
from app.schemas.product import Product


def map_product_model_to_schema(
    product_model: ProductModel,
) -> Product:
    return Product(
        id=product_model.product_id,
        name=product_model.name,
        category=product_model.category,
        brand=product_model.brand,
        price=float(product_model.price),
        currency=product_model.currency,
        description=product_model.description,
        features=list(product_model.features),
        stock=product_model.stock,
        rating=float(product_model.rating),
    )


def get_active_products(
    session: Session,
) -> list[Product]:
    product_models = list_active_products(session)

    return [
        map_product_model_to_schema(product_model)
        for product_model in product_models
    ]