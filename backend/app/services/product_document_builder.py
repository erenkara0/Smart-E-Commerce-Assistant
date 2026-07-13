from app.schemas.product import Product


def build_product_document(product: Product) -> str:
    features = ", ".join(product.features)

    return (
        f"Ürün ID: {product.id}\n"
        f"Ürün adı: {product.name}\n"
        f"Kategori: {product.category}\n"
        f"Marka: {product.brand}\n"
        f"Fiyat: {product.price} {product.currency}\n"
        f"Stok: {product.stock}\n"
        f"Puan: {product.rating}\n"
        f"Açıklama: {product.description}\n"
        f"Özellikler: {features}"
    )


def build_product_documents(products: list[Product]) -> list[str]:
    return [build_product_document(product) for product in products]