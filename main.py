import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

from src.database.db import Database
from src.api.api import GeminiAPI
#from src.Vector_store.faiss_store import VectorStore
#from src.Vector_store.milvus_store import VectorStore
from src.Vector_store.qdrant_store import VectorStore
from src.cache.cache import SemanticCache
from src.utils.sql_utils import is_read_only

def main():
    db = Database()
    db.connect()
    schema_info = db.get_schema_info_with_comments()
    #print(f"[SCHEMA INFO] {schema_info}")
    vector_store = VectorStore(schema_info)
    gemini = GeminiAPI()
    semantic_cache = SemanticCache()

    print("Welcome to AI Agent! Type 'exit' to quit.")
    while True:
        question = input("Ask a question (or 'exit'): ")

        if question.lower() == "exit":
            break

        # Step 1: Check semantic cache
        sql_query = semantic_cache.lookup(question)
        if sql_query:
            print(f"[SEMANTIC CACHE HIT] SQL: {sql_query}")
        else:
            # Step 2: Use vector search on schema
            schema_context = [text for text, _ in vector_store.search(question, k=6)]  # No normalization
            # Step 2b: Get top correction pairs
            top_corrections = vector_store.get_top_corrections(question, top_n=3)
            print(f"[VECTOR SEARCH] Context: {schema_context}")
            print(f"[CORRECTIONS] Top pairs: {top_corrections}")

            # Step 3: Use LLM to generate SQL, pass corrections too
            sql_query = gemini.generate_sql_query(question, schema_context, top_corrections)
            print(f"[LLM GENERATED] SQL: {sql_query}")

            # Step 4: Save to semantic cache
            semantic_cache.add(question, sql_query)

        # Step 5: Check if SQL is safe
        if not is_read_only(sql_query):
            print("[BLOCKED] Only SELECT queries are allowed. Unsafe query skipped.")
            continue

        # Step 6: Execute SQL
        try:
            results = db.query(sql_query)
        except Exception as e:
            print(f"[SQL ERROR] {e}")
            continue

        # Step 7: Generate answer
        answer = gemini.friendly_answer(results, question)
        print(f"[BOT]: {answer}")

    db.close()

if __name__ == "__main__":
    main()