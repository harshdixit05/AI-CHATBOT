import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

class VectorStore:
    def __init__(self, schema_info):
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.dimension = 384
        self.index = faiss.IndexFlatL2(self.dimension)
        self.texts = []  # holds schema texts like "Table users has columns: id, name"
        self.metadata = []  # holds (table, columns)
        self._add_schema(schema_info)

    def _add_schema(self, schema_info):
        # schema_info: list of (table, [columns])
        texts = [f"Table {table} has columns: {', '.join(cols)}" for table, cols in schema_info]
        embeddings = self.model.encode(texts)
        self.index.add(np.array(embeddings).astype('float32'))
        self.texts.extend(texts)
        self.metadata.extend(schema_info)

    def search(self, query, k=2):
        q_emb = self.model.encode([query]).astype('float32')
        D, I = self.index.search(q_emb, k)
        results = []
        for idx in I[0]:
            results.append((self.texts[idx], self.metadata[idx]))
        return results