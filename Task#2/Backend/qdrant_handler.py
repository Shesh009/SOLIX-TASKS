from qdrant_client.http.models import Filter

class QdrantHandler:
    def __init__(self, collection_name="pdf_rag", embeddings=None, QdrantManager=None):
        self.collection_name = collection_name
        self.embeddings = embeddings
        self.qdrant_manager = QdrantManager(collection_name=collection_name, embeddings=embeddings)

    def delete_collection(self):
        try:
            self.qdrant_manager.delete_collection()
        except ValueError as e:
            print(f"Error deleting collection: {e}")

    def add_embeddings(self):
        try:
            self.qdrant_manager.add_embeddings()
        except ValueError as e:
            print(f"Error adding texts to Qdrant: {e}")

    def search_similar(self, query_vector, top_k=10, filters: Filter = None, score_threshold=None):
        try:
            results = self.qdrant_manager.search(
                query_vector=query_vector,
                top_k=top_k,
                filters=filters
            )

            if score_threshold is not None:
                results = [r for r in results if r.score >= score_threshold]

            return results

        except ValueError as e:
            print(f"Error searching in Qdrant: {e}")
            return []