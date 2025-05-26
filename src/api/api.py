
import google.generativeai as genai
from src.database.Schema import SCHEMA_HINT
from dotenv import load_dotenv
import os

class GeminiAPI:
    def __init__(self):
        # Load environment variables from .env
        load_dotenv()

        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("API_KEY not found in environment variables.")

        # Assuming genai is your imported Gemini SDK/module
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-2.0-flash')
    def generate_sql_query(self, user_input):
        prompt = (
           "You are an expert MySQL assistant.\n"
        "Given the following user request, generate a single valid MySQL query using the provided schema.\n"
        "Return ONLY the SQL query as plain text, with NO code block markers, no triple backticks, and no language tags.\n"
        "Do not include any explanation, comments, or extra text—only the SQL query.\n\n"
        f"User request: {user_input}\n"
        f"Schema:\n{SCHEMA_HINT}\n"
        "SQL Query:"
        )
        response = self.model.generate_content(prompt)
        return response.text.strip()
    

    

    def friendly_one_line_answer(self, sql_output, user_input):
        prompt = (
            f"User asked: '{user_input}'.\n"
            f"Database output: {sql_output}\n"
            f"Reply with a friendly.dont include *"
        )
        response = self.model.generate_content(prompt)
        return response.text.strip()