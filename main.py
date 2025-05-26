from src.database.db import Database
from src.api.api import GeminiAPI
from src.Vector_store.Vector import VectorStore
import re

def main():
    db = Database()
    db.connect()  # Connect to the database
    schema_info = db.get_schema_info()
    vector_store = VectorStore(schema_info)

    gemini = GeminiAPI()

    print("Welcome to the GYM Fitness AI Agent! Type 'exit' to quit.")
    while True:
        question = input("Ask a question (or 'exit'): ")
        if question.lower() == "exit":
            break
        # 1. Vector search for relevant schema
        schema_context = vector_store.search(question, k=2)
        # 2. Generate SQL with LLM
        sql_query = gemini.generate_sql_query(question, schema_context)
        print(f"Generated SQL: {sql_query}")


        # 3. Run SQL and get answer
        try:
            results = db.query(sql_query)
        except Exception as e:
            print(f"SQL Error: {e}")
            continue
        # 4. Friendly answer
        answer = gemini.friendly_answer(results, question)
        print(answer)

    db.close()

if __name__ == "__main__":
    main()