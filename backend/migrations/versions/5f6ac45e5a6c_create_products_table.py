"""Create products table.

Revision ID: 5f6ac45e5a6c
Revises:
Create Date: 2026-07-31
"""

from collections.abc import Sequence

from alembic import op
import sqlalchemy as sa


revision: str = "5f6ac45e5a6c"
down_revision: str | Sequence[str] | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "products",
        sa.Column(
            "id",
            sa.Integer(),
            autoincrement=True,
            nullable=False,
        ),
        sa.Column(
            "product_id",
            sa.String(length=100),
            nullable=False,
        ),
        sa.Column(
            "sku",
            sa.String(length=100),
            nullable=False,
        ),
        sa.Column(
            "name",
            sa.String(length=200),
            nullable=False,
        ),
        sa.Column(
            "category",
            sa.String(length=100),
            nullable=False,
        ),
        sa.Column(
            "brand",
            sa.String(length=100),
            nullable=False,
        ),
        sa.Column(
            "price",
            sa.Numeric(
                precision=12,
                scale=2,
            ),
            nullable=False,
        ),
        sa.Column(
            "currency",
            sa.String(length=3),
            nullable=False,
        ),
        sa.Column(
            "description",
            sa.Text(),
            nullable=False,
        ),
        sa.Column(
            "features",
            sa.JSON(),
            nullable=False,
        ),
        sa.Column(
            "stock",
            sa.Integer(),
            nullable=False,
        ),
        sa.Column(
            "rating",
            sa.Numeric(
                precision=3,
                scale=2,
            ),
            nullable=False,
        ),
        sa.Column(
            "image_url",
            sa.Text(),
            nullable=True,
        ),
        sa.Column(
            "product_url",
            sa.Text(),
            nullable=True,
        ),
        sa.Column(
            "is_active",
            sa.Boolean(),
            nullable=False,
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.CheckConstraint(
            "price > 0",
            name="ck_products_price_positive",
        ),
        sa.CheckConstraint(
            "stock >= 0",
            name="ck_products_stock_non_negative",
        ),
        sa.CheckConstraint(
            "rating >= 0 AND rating <= 5",
            name="ck_products_rating_range",
        ),
        sa.PrimaryKeyConstraint(
            "id",
            name="pk_products",
        ),
        sa.UniqueConstraint(
            "product_id",
            name="uq_products_product_id",
        ),
        sa.UniqueConstraint(
            "sku",
            name="uq_products_sku",
        ),
    )

    op.create_index(
        "ix_products_active_category",
        "products",
        [
            "is_active",
            "category",
        ],
        unique=False,
    )

    op.create_index(
        "ix_products_active_brand",
        "products",
        [
            "is_active",
            "brand",
        ],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index(
        "ix_products_active_brand",
        table_name="products",
    )

    op.drop_index(
        "ix_products_active_category",
        table_name="products",
    )

    op.drop_table("products")