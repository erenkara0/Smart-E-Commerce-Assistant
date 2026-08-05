from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import ProductModel


def list_active_products(
    session: Session,
) -> list[ProductModel]:
    statement = (
        select(ProductModel)
        .where(ProductModel.is_active.is_(True))
        .order_by(ProductModel.product_id.asc())
    )

    return list(
        session.scalars(statement).all()
    )