from pydantic import BaseModel, Field


class Product(BaseModel):
    id: str = Field(
        ...,
        description="Unique product identifier.",
        examples=["prd-001"],
    )
    name: str = Field(
        ...,
        min_length=1,
        max_length=200,
        description="Product name.",
        examples=["Lenovo IdeaPad Gaming 3"],
    )
    category: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="Product category.",
        examples=["Laptop"],
    )
    brand: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="Product brand.",
        examples=["Lenovo"],
    )
    price: float = Field(
        ...,
        gt=0,
        description="Product price.",
        examples=[32999.99],
    )
    currency: str = Field(
        default="TRY",
        min_length=3,
        max_length=3,
        description="Currency code.",
        examples=["TRY"],
    )
    description: str = Field(
        ...,
        min_length=1,
        description="Short product description.",
        examples=["Gaming and daily use focused laptop."],
    )
    features: list[str] = Field(
        default_factory=list,
        description="Product feature list.",
        examples=[["16 GB RAM", "512 GB SSD", "RTX 4050"]],
    )
    stock: int = Field(
        ...,
        ge=0,
        description="Available stock quantity.",
        examples=[15],
    )
    rating: float = Field(
        ...,
        ge=0,
        le=5,
        description="Average product rating between 0 and 5.",
        examples=[4.6],
    )