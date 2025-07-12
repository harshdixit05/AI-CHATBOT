import os
from pymilvus import connections, Collection, CollectionSchema, FieldSchema, DataType, utility
from sentence_transformers import SentenceTransformer
from sentence_transformers.util import cos_sim
from dotenv import load_dotenv
from src.utils.correction import load_corrections

# Load environment variables
load_dotenv()

class VectorStore:
    def __init__(self, schema_info_dict):
        # Load from .env
        host = os.getenv("MILVUS_HOST", "localhost")
        port = os.getenv("MILVUS_PORT", "19530")
        self.collection_name = os.getenv("MILVUS_COLLECTION", "schema_store")
        model_name = os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")

        # Connect and drop old collection
        connections.connect("default", host=host, port=port)
        if utility.has_collection(self.collection_name):
            utility.drop_collection(self.collection_name)

        # Load corrections (only for LLM prompt)
        corrections_path = os.path.join(os.path.dirname(__file__), "..", "..", "data", "correction.txt")
        self.corrections = load_corrections(os.path.abspath(corrections_path))

        self.model = SentenceTransformer(model_name)
        self._create_schema()
        self._add_schema(schema_info_dict)

    def _create_schema(self):
        fields = [
            FieldSchema(name="id", dtype=DataType.INT64, is_primary=True, auto_id=True),
            FieldSchema(name="embedding", dtype=DataType.FLOAT_VECTOR, dim=384),
            FieldSchema(name="text", dtype=DataType.VARCHAR, max_length=1024),
            FieldSchema(name="table", dtype=DataType.VARCHAR, max_length=128),
            FieldSchema(name="columns", dtype=DataType.VARCHAR, max_length=512),
        ]

        schema = CollectionSchema(fields, description="Schema collection")
        self.collection = Collection(name=self.collection_name, schema=schema)

        self.collection.create_index(
            field_name="embedding",
            index_params={
                "index_type": "IVF_FLAT",
                "metric_type": "COSINE",  
                "params": {"nlist": 128}
            }
        )

        self.collection.load()

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

        self.collection.insert([
            embeddings,
            texts,
            table_names,
            column_texts
        ])
        self.collection.flush()

    def search(self, query, k=6):
        # No normalization/correction here
        q_emb = self.model.encode([query]).tolist()

        self.collection.load()

        results = self.collection.search(
            data=q_emb,
            anns_field="embedding",
            param={"metric_type": "COSINE", "params": {"nprobe": 10}},
            limit=k,
            output_fields=["text", "table", "columns"]
        )

        matches = []
        seen = set()
        for hit in results[0]:
            text = hit.entity.get("text")
            table = hit.entity.get("table")
            columns_str = hit.entity.get("columns") or ""
            columns = [col.strip() for col in columns_str.split(",") if col.strip()]
            key = (table, tuple(columns))
            if key not in seen:
                matches.append((text, (table, columns)))
                seen.add(key)
        return matches

    def get_top_corrections(self, query, top_n=3):
        """
        Returns the top-N most relevant correction pairs for the query.
        """
        if not self.corrections:
            return []

        # Flatten corrections into pairs
        pairs = [(k, v) for k, v in self.corrections.items()]
        keys = [k for k, v in pairs]
        if not keys:
            return []

        # Embed query and correction keys
        query_emb = self.model.encode([query])
        keys_emb = self.model.encode(keys)

        # Compute cosine similarity
        sims = cos_sim(query_emb, keys_emb)[0].tolist()
        # Get top N indices
        top_indices = sorted(range(len(sims)), key=lambda i: sims[i], reverse=True)[:top_n]
        # Return top-N pairs
        return [pairs[i] for i in top_indices]