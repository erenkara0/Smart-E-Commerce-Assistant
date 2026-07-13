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

    def search(self, query: str, limit: int = 5) -> list[dict[str, str | int]]:
        normalized_query = query.strip().casefold()

        if not normalized_query:
            return []

        documents = self.get_documents()
        query_terms = normalized_query.split()
        scored_results: list[dict[str, str | int]] = []

        for document in documents:
            normalized_document = document.casefold()
            score = sum(
                normalized_document.count(term)
                for term in query_terms
            )

            if score > 0:
                scored_results.append(
                    {
                        "document": document,
                        "score": score,
                    }
                )

        scored_results.sort(
            key=lambda result: int(result["score"]),
            reverse=True,
        )

        return scored_results[:limit]

    def clear(self) -> None:
        self.documents = []


vector_store_service = InMemoryVectorStoreService()