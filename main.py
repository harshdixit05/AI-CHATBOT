from src.database.db import Database
from src.api.api import GeminiAPI

def main():
    db = Database()
    db.connect()  # Connect to the database

    gemini = GeminiAPI()

    print("Welcome to the Olympic Athletes AI Agent! Type 'exit' to quit.")
    while True:
        user_input = input("Ask your question: ")
        if user_input.lower() == 'exit':
            break

        # 1. Generate SQL query from user question
        sql_query = gemini.generate_sql_query(user_input)
        print(f"Generated SQL: {sql_query}")

        try:
            # 2. Run the generated SQL query
            result = db.query(sql_query)
        except Exception as e:
            print(f"SQL Error: {e}")
            continue

        # 3. Get a friendly one-line answer from Gemini
        answer = gemini.friendly_one_line_answer(result, user_input)
        print(f"AI Answer: {answer}")

    db.close()

if __name__ == "__main__":
    main()