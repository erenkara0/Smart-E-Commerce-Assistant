class InMemoryVectorStoreService:
    def __init__(self) -> None:
        self.documents: list[str] = []

    def build_index(
        self,
        documents: list[str],
    ) -> list[str]:
        self.documents = list(documents)

        return list(self.documents)

    def get_documents(self) -> list[str]:
        return list(self.documents)

    def search(
        self,
        query: str,
        limit: int = 5,
    ) -> list[dict[str, str | int]]:
        normalized_query = query.strip().casefold()

        if not normalized_query:
            return []

        query_terms = normalized_query.split()
        scored_results: list[
            dict[str, str | int]
        ] = []

        for document in self.get_documents():
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