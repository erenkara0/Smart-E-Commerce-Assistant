import json
from pathlib import Path
from pydantic import ValidationError
from app.schemas.product import Product

PRODUCTS_PATH = Path(__file__).resolve().parents[1] / "data" / "products.json"

def load_products(file_path: Path = PRODUCTS_PATH) -> list[Product]:
    if not file_path.exists():
        raise FileNotFoundError(f"Product data file not found: {file_path}")

    try:
        with file_path.open("r", encoding="utf-8") as file:
            products_data = json.load(file)
    except json.JSONDecodeError as exc:
        raise ValueError("Product data file contains invalid JSON.") from exc

    if not isinstance(products_data, list):
        raise ValueError("Product data must be a list.")

    try:
        return [Product.model_validate(product) for product in products_data]
    except ValidationError as exc:
        raise ValueError("Product data validation failed.") from exc