from decimal import Decimal
from enum import StrEnum
from typing import Any

from pydantic import (
    AnyHttpUrl,
    BaseModel,
    ConfigDict,
    Field,
    field_validator,
)


class SupportedCurrency(StrEnum):
    TRY = "TRY"
    USD = "USD"
    EUR = "EUR"


class ExcelProductRow(BaseModel):
    model_config = ConfigDict(
        str_strip_whitespace=True,
        extra="forbid",
        use_enum_values=True,
    )

    product_id: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="Stable product identifier used by the application.",
        examples=["prd-001"],
    )
    sku: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="Unique store stock keeping unit.",
        examples=["LNV-IPG3-001"],
    )
    name: str = Field(
        ...,
        min_length=1,
        max_length=200,
        description="Product name displayed to customers.",
        examples=["Lenovo IdeaPad Gaming 3"],
    )
    category: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="Primary product category.",
        examples=["Laptop"],
    )
    brand: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="Product brand.",
        examples=["Lenovo"],
    )
    price: Decimal = Field(
        ...,
        gt=0,
        max_digits=12,
        decimal_places=2,
        description="Current product selling price.",
        examples=[Decimal("32999.99")],
    )
    currency: SupportedCurrency = Field(
        default=SupportedCurrency.TRY,
        description="ISO-style currency code supported by the importer.",
        examples=[SupportedCurrency.TRY],
    )
    description: str = Field(
        ...,
        min_length=1,
        max_length=5000,
        description="Customer-facing product description.",
    )
    features: list[str] = Field(
        ...,
        min_length=1,
        description="Normalized product feature collection.",
        examples=[
            [
                "Ryzen 5",
                "16 GB RAM",
                "512 GB SSD",
                "RTX 4050",
            ]
        ],
    )
    stock: int = Field(
        ...,
        ge=0,
        description="Available stock quantity.",
        examples=[12],
    )
    rating: Decimal = Field(
        ...,
        ge=0,
        le=5,
        max_digits=3,
        decimal_places=2,
        description="Product rating between zero and five.",
        examples=[Decimal("4.5")],
    )
    image_url: AnyHttpUrl | None = Field(
        default=None,
        description="Optional product image URL.",
    )
    product_url: AnyHttpUrl | None = Field(
        default=None,
        description="Optional store product detail URL.",
    )
    is_active: bool = Field(
        default=True,
        description="Whether the product can be used in customer searches.",
    )

    @field_validator("currency", mode="before")
    @classmethod
    def normalize_currency(cls, value: Any) -> Any:
        if isinstance(value, str):
            return value.strip().upper()

        return value

    @field_validator("features", mode="before")
    @classmethod
    def normalize_features(cls, value: Any) -> list[str]:
        if isinstance(value, str):
            normalized_features = [
                feature.strip()
                for feature in value.split("|")
                if feature.strip()
            ]
        elif isinstance(value, (list, tuple)):
            normalized_features = [
                str(feature).strip()
                for feature in value
                if str(feature).strip()
            ]
        else:
            raise ValueError(
                "Features must be text separated by '|' characters."
            )

        unique_features = list(dict.fromkeys(normalized_features))

        if not unique_features:
            raise ValueError(
                "At least one product feature must be provided."
            )

        return unique_features

    @field_validator("image_url", "product_url", mode="before")
    @classmethod
    def normalize_optional_url(cls, value: Any) -> Any:
        if value is None:
            return None

        if isinstance(value, str) and not value.strip():
            return None

        return value

    @field_validator("is_active", mode="before")
    @classmethod
    def normalize_active_status(cls, value: Any) -> bool:
        if isinstance(value, bool):
            return value

        if isinstance(value, str):
            normalized_value = value.strip().upper()

            if normalized_value == "TRUE":
                return True

            if normalized_value == "FALSE":
                return False

        raise ValueError(
            "Active status must be TRUE or FALSE."
        )

    @field_validator("price", "stock", "rating", mode="before")
    @classmethod
    def reject_boolean_numeric_values(cls, value: Any) -> Any:
        if isinstance(value, bool):
            raise ValueError(
                "Boolean values cannot be used in numeric fields."
            )

        return value


class ProductImportValidationError(BaseModel):
    row: int = Field(
        ...,
        ge=2,
        description="Excel worksheet row containing the error.",
    )
    field: str | None = Field(
        default=None,
        description="Product field related to the validation error.",
    )
    message: str = Field(
        ...,
        min_length=1,
        description="Human-readable validation error.",
    )


class ProductExcelParseResult(BaseModel):
    products: list[ExcelProductRow] = Field(
        default_factory=list,
    )
    total_rows: int = Field(
        default=0,
        ge=0,
    )
    valid_rows: int = Field(
        default=0,
        ge=0,
    )
    failed_rows: int = Field(
        default=0,
        ge=0,
    )
    errors: list[ProductImportValidationError] = Field(
        default_factory=list,
    )