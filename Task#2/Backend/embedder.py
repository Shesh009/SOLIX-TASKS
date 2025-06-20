from sentence_transformers import SentenceTransformer

class Embedder:
    def __init__(self, model_name='all-MiniLM-L6-v2'):
        self.model = SentenceTransformer(model_name)

    def generate_embeddings(self, text_chunks):
        embeddings = []
        for chunk in text_chunks:
            embedding = self.model.encode(chunk).tolist()
            embeddings.append((chunk, embedding))
        return embeddings
    
    def embed_query(self, query):
        return self.model.encode(query).tolist()