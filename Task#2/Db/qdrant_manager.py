from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance
from qdrant_client.http.models import Filter

class QdrantManager:
    def __init__(self, collection_name = "pdf_rag", embeddings = None):
        self.collection_name = collection_name
        self.client = QdrantClient(url="http://localhost:6333")
        self._ensure_collection()
        self.embeddings = embeddings

    def _ensure_collection(self):
            try:
                self.client.get_collection(self.collection_name)
            except Exception as e:
                try:
                    self.client.create_collection(
                        collection_name=self.collection_name,
                        vectors_config=VectorParams(size=384, distance=Distance.COSINE)
                    )
                except Exception as e:
                    raise ValueError("Failed to create or access Qdrant collection.")
                
    def delete_collection(self):
        try:
            self.client.get_collection(self.collection_name)
            self.client.delete_collection(self.collection_name)
            print(f"Collection '{self.collection_name}' deleted successfully.")
        except Exception as e:
            print(f"Collection '{self.collection_name}' does not exist or could not be deleted. Error: {e}")
                
    def add_embeddings(self):
            try:
                self._ensure_collection()
                points = [
                    {
                        "id": i,
                        "vector": emb,
                        "payload": {"text": text}
                    }
                    for i, (text, emb) in enumerate(self.embeddings)
                ]
                
                self.client.upsert(collection_name=self.collection_name, points=points)
            except Exception as e:
                raise ValueError(f"Failed to add texts to Qdrant. Error: {e}")
    
    def search(self, query_vector, top_k=10, filters: Filter = None):
        try:
            return self.client.search(
                collection_name=self.collection_name,
                query_vector=query_vector,
                limit=top_k,
                with_payload=True
            )
        except Exception as e:
            print(f"[QdrantManager] Search failed: {e}")
            return []
    