import google.generativeai as genai

from dotenv import load_dotenv
import os
import re
from src.utils.sql_utils import clean_sql

load_dotenv()

class GeminiAPI:
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables.")
        
        genai.configure(api_key=api_key)

        model_name = os.getenv("GEMINI_MODEL") 
        self.model = genai.GenerativeModel(model_name)
        

    def generate_sql_query(self, user_input, schema_context, top_corrections=None):
        schema_descriptions = "\n".join(schema_context)

        prompt = f"""Database Schema:
{schema_descriptions}

Instructions:
- Use only the tables and columns exactly as shown in the schema above.
- Do not guess or invent table or column names.
- Use only SELECT statements. Do not modify, delete, or insert data.
- Output only the SQL query — no explanations, no comments, and no code block markers.
- Output must be plain SQL ready to run in a MySQL database.
"""

        if top_corrections:
            prompt += "\nSynonym corrections (use these mappings for alternate names):\n"
            for k, v in top_corrections:
                prompt += f"- {k} → {v}\n"
            prompt += "\n"

        prompt += f"User question: {user_input}\n"

        response = self.model.generate_content(prompt)
        raw_sql = response.text.strip()
        cleaned_sql = clean_sql(raw_sql)
        return cleaned_sql

    def friendly_answer(self, sql_output, user_input):
        prompt = (
            f"User asked: '{user_input}'.\n"
            f"Database output: {sql_output}\n"
            f"Reply with a short friendly."
        )

        response = self.model.generate_content(prompt)
        return response.text.strip()