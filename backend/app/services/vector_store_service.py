from app.services.product_document_builder import build_product_documents
from app.services.product_loader import load_products


class InMemoryVectorStoreService:
    def __init__(self) -> None:
        self.documents: list[str] = []

    def build_index(self) -> list[str]:
        products = load_products()
        self.documents = build_product_documents(products)
        return self.documents

    def get_documents(self) -> list[str]:
        if not self.documents:
            return self.build_index()

        return self.documents

    def clear(self) -> None:
        self.documents = []


vector_store_service = InMemoryVectorStoreService()