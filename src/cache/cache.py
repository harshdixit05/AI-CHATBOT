import faiss
import numpy as np
import pickle
from sentence_transformers import SentenceTransformer
import os
from dotenv import load_dotenv


load_dotenv()


class SemanticCache:
    def __init__(self):
        self.model = os.getenv("EMBEDDING_MODEL")
        self.embedding_dim = int(os.getenv("EMBEDDING_DIM"))
        self.index_type = os.getenv("FAISS_INDEX_TYPE")

        self.model = SentenceTransformer(self.model)

        # Dynamically create index
        if self.index_type.lower() == "flatip":
            self.index = faiss.IndexFlatIP(self.embedding_dim)
        else:  # default: L2
            self.index = faiss.IndexFlatL2(self.embedding_dim)

        self.cache = []

    def add(self, query, sql):
        embedding = self.model.encode([query]).astype('float32')
        self.index.add(embedding)
        self.cache.append((query, sql))

    def lookup(self, query, threshold=0.85):
        if len(self.cache) == 0:
            return None
        emb = self.model.encode([query]).astype('float32')
        D, I = self.index.search(emb, 1)
        sim = 1 - D[0][0]  # similarity from distance
        if sim > threshold:
            return self.cache[I[0][0]][1]
        return None


