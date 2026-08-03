from datetime import datetime
from decimal import Decimal

from sqlalchemy import (
    JSON,
    Boolean,
    CheckConstraint,
    DateTime,
    Index,
    Integer,
    Numeric,
    String,
    Text,
    UniqueConstraint,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class ProductModel(Base):
    __tablename__ = "products"

    __table_args__ = (
        UniqueConstraint(
            "product_id",
            name="uq_products_product_id",
        ),
        UniqueConstraint(
            "sku",
            name="uq_products_sku",
        ),
        CheckConstraint(
            "price > 0",
            name="ck_products_price_positive",
        ),
        CheckConstraint(
            "stock >= 0",
            name="ck_products_stock_non_negative",
        ),
        CheckConstraint(
            "rating >= 0 AND rating <= 5",
            name="ck_products_rating_range",
        ),
        Index(
            "ix_products_active_category",
            "is_active",
            "category",
        ),
        Index(
            "ix_products_active_brand",
            "is_active",
            "brand",
        ),
    )

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    product_id: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    sku: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    name: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
    )

    category: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    brand: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    price: Mapped[Decimal] = mapped_column(
        Numeric(
            precision=12,
            scale=2,
        ),
        nullable=False,
    )

    currency: Mapped[str] = mapped_column(
        String(3),
        nullable=False,
        default="TRY",
    )

    description: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    features: Mapped[list[str]] = mapped_column(
        JSON,
        nullable=False,
        default=list,
    )

    stock: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    rating: Mapped[Decimal] = mapped_column(
        Numeric(
            precision=3,
            scale=2,
        ),
        nullable=False,
    )

    image_url: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    product_url: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )