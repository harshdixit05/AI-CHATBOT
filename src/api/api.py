
import google.generativeai as genai
from src.database.Schema import SCHEMA_HINT
from dotenv import load_dotenv
import os
import re

class GeminiAPI:
    def __init__(self):

        # Load environment variables from .env
        load_dotenv()

        api_key = "GEMINI_API_KEY"
       
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-2.0-flash')


        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("API_KEY not found in environment variables.")

        # Assuming genai is your imported Gemini SDK/module
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-2.0-flash')
   
    def clean_sql(self, sql):
        # Remove code block markers and triple quotes (```sql, ```, """sql, etc.)
        sql = re.sub(r'^[`"]{3,}.*$', '', sql, flags=re.MULTILINE)
        sql = sql.replace('```', '').replace('"""', '')
        # Remove leading/trailing whitespace
        return sql.strip()

    def generate_sql_query(self, user_input, schema_context):
        schema_descriptions = "\n".join([s for s, _ in schema_context])
        prompt = f"""Database Schema:\n{schema_descriptions}
User question: {user_input}
Write only the SQL query (MySQL syntax) that answers the user's question. Return only the SQL query, with no explanations and no code block markers (such as ```sql). The output should be plain SQL so it can be run in database, nothing else.
"""
        response = self.model.generate_content(prompt)
        raw_sql = response.text.strip()
        cleaned_sql = self.clean_sql(raw_sql)
        return cleaned_sql
    

   

 
    

    def friendly_answer(self, sql_output, user_input):
        prompt = (
            f"User asked: '{user_input}'.\n"
            f"Database output: {sql_output}\n"
            f"Reply with a friendly.dont include *"
        )

        response = self.model.generate_content(prompt)
        return response.text.strip()
