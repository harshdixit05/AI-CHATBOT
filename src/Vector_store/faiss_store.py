import os
import faiss
import pickle
import numpy as np
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
from sentence_transformers.util import cos_sim
from src.utils.correction import load_corrections

# Load environment variables
load_dotenv()

class VectorStore:
    def __init__(self, schema_info_dict):
        self.index_path = os.getenv("FAISS_INDEX_PATH", "faiss_index.index")
        self.data_path = os.getenv("FAISS_DATA_PATH", "faiss_metadata.pkl")
        model_name = os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")

        # Load corrections (only for LLM prompt)
        corrections_path = os.path.join(os.path.dirname(__file__), "..", "..", "data", "correction.txt")
        self.corrections = load_corrections(os.path.abspath(corrections_path))

        self.model = SentenceTransformer(model_name)
        self.schema_info_dict = schema_info_dict
        self.index = None
        self.metadata = []

        self._create_index()
        self._add_schema(schema_info_dict)

    def _create_index(self):
        dim = 384  
        self.index = faiss.IndexFlatIP(dim)  

    def _add_schema(self, schema_info_dict):
        texts = []
        table_names = []
        column_texts = []

        for table, columns in schema_info_dict.items():
            col_names = [col['name'] for col in columns]
            texts.append(f"Table {table} has columns: {', '.join(col_names)}")
            table_names.append(table)
            column_texts.append(", ".join(col_names))

        embeddings = self.model.encode(texts, normalize_embeddings=True)
        self.index.add(np.array(embeddings).astype("float32"))

        # Save metadata for lookup
        self.metadata = [
            {
                "text": texts[i],
                "table": table_names[i],
                "columns": column_texts[i]
            } for i in range(len(texts))
        ]

        # Optional: Save index and metadata to disk
        faiss.write_index(self.index, self.index_path)
        with open(self.data_path, "wb") as f:
            pickle.dump(self.metadata, f)

    def search(self, query, k=6):
        query_emb = self.model.encode([query], normalize_embeddings=True)
        query_np = np.array(query_emb).astype("float32")

        distances, indices = self.index.search(query_np, k)

        matches = []
        seen = set()
        for idx in indices[0]:
            if idx < len(self.metadata):
                meta = self.metadata[idx]
                table = meta["table"]
                columns = [col.strip() for col in meta["columns"].split(",") if col.strip()]
                key = (table, tuple(columns))
                if key not in seen:
                    matches.append((meta["text"], (table, columns)))
                    seen.add(key)
        return matches

    def get_top_corrections(self, query, top_n=3):
        if not self.corrections:
            return []

        pairs = [(k, v) for k, v in self.corrections.items()]
        keys = [k for k, v in pairs]
        if not keys:
            return []

        query_emb = self.model.encode([query])
        keys_emb = self.model.encode(keys)

        sims = cos_sim(query_emb, keys_emb)[0].tolist()
        top_indices = sorted(range(len(sims)), key=lambda i: sims[i], reverse=True)[:top_n]
        return [pairs[i] for i in top_indices]
