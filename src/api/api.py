import os
import google.generativeai as genai

class GeminiAPI:
    def __init__(self):
        
        api_key = "AIzaSyDUAGuHeoVMVM4DGEH4AnG6b7S2sMebPv"
       
        genai.configure(api_key="AIzaSyDUAGuHeoVMVM4DGEH4AnG6b7S2sMebPvs")
        self.model = genai.GenerativeModel('gemini-2.0-flash')

    def generate_sql_query(self, user_input, table_schema_hint="athletes(Name TEXT, Sex TEXT, Age INT, Height FLOAT, Weight FLOAT, Team TEXT, NOC TEXT, Games TEXT, Year INT, Season TEXT, City TEXT, Sport TEXT, Event TEXT, Medal TEXT)"):
        prompt = (
            f"You are an expert MySQL assistant. Given the user request, generate a valid SQL query for the 'athletes' table. "
            f"Table schema: {table_schema_hint}\n"
            f"User request: {user_input}\n"
            f"Return ONLY the SQL query as plain text, with NO code block markers, no triple backticks, and no language tags."
        )
        response = self.model.generate_content(prompt)
        return response.text.strip()
    

    

    def friendly_one_line_answer(self, sql_output, user_input):
        prompt = (
            f"User asked: '{user_input}'.\n"
            f"Database output: {sql_output}\n"
            f"Reply with a friendly."
        )
        response = self.model.generate_content(prompt)
        return response.text.strip()