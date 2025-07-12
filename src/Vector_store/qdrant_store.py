import os
from sentence_transformers import SentenceTransformer
from sentence_transformers.util import cos_sim
from qdrant_client import QdrantClient
from qdrant_client.models import (
    VectorParams,
    Distance,
    PointStruct,
    FieldCondition,
    MatchValue,
    Filter,
)
from dotenv import load_dotenv
from src.utils.correction import load_corrections

# Load environment variables
load_dotenv()

class VectorStore:
    def __init__(self, schema_info_dict):
        self.collection_name = os.getenv("QDRANT_COLLECTION", "schema_store")
        model_name = os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")

        # Qdrant client setup
        host = os.getenv("QDRANT_HOST", "localhost")
        port = int(os.getenv("QDRANT_PORT", "6333"))
        self.client = QdrantClient(host=host, port=port)

        # Load corrections (only for LLM prompt)
        corrections_path = os.path.join(os.path.dirname(__file__), "..", "..", "data", "correction.txt")
        self.corrections = load_corrections(os.path.abspath(corrections_path))

        self.model = SentenceTransformer(model_name)

        # Drop and recreate collection
        if self.client.collection_exists(collection_name=self.collection_name):
            self.client.delete_collection(collection_name=self.collection_name)

        self._create_collection()
        self._add_schema(schema_info_dict)

    def _create_collection(self):
        self.client.create_collection(
            collection_name=self.collection_name,
            vectors_config=VectorParams(
                size=384,
                distance=Distance.COSINE
            )
        )

    def _add_schema(self, schema_info_dict):
        texts = []
        table_names = []
        column_texts = []

        for table, columns in schema_info_dict.items():
            col_names = [col['name'] for col in columns]
            texts.append(f"Table {table} has columns: {', '.join(col_names)}")
            table_names.append(table)
            column_texts.append(", ".join(col_names))

        embeddings = self.model.encode(texts).tolist()

        points = []
        for i, (emb, text, table, columns) in enumerate(zip(embeddings, texts, table_names, column_texts)):
            points.append(PointStruct(
                id=i,
                vector=emb,
                payload={
                    "text": text,
                    "table": table,
                    "columns": columns
                }
            ))

        self.client.upsert(
            collection_name=self.collection_name,
            points=points
        )

    def search(self, query, k=6):
        q_emb = self.model.encode([query])[0]

        search_result = self.client.search(
            collection_name=self.collection_name,
            query_vector=q_emb,
            limit=k,
            with_payload=True
        )

        matches = []
        seen = set()

        for hit in search_result:
            payload = hit.payload
            text = payload.get("text", "")
            table = payload.get("table", "")
            columns_str = payload.get("columns", "")
            columns = [col.strip() for col in columns_str.split(",") if col.strip()]
            key = (table, tuple(columns))
            if key not in seen:
                matches.append((text, (table, columns)))
                seen.add(key)

        return matches

    def get_top_corrections(self, query, top_n=3):
        if not self.corrections:
            return []

        pairs = [(k, v) for k, v in self.corrections.items()]
        keys = [k for k, _ in pairs]
        if not keys:
            return []

        query_emb = self.model.encode([query])
        keys_emb = self.model.encode(keys)
        sims = cos_sim(query_emb, keys_emb)[0].tolist()

        top_indices = sorted(range(len(sims)), key=lambda i: sims[i], reverse=True)[:top_n]
        return [pairs[i] for i in top_indices]
