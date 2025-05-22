import logging
import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables from .env file in src/api/
env_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path=env_path)

# Ensure the logs directory exists
log_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), '..', 'logs')
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

# Configure logging
logging.basicConfig(
    filename=os.path.join(log_dir, 'api.log'),
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class GeminiAPI:
    def __init__(self):
        self.api_key = os.getenv('GEMINI_API_KEY')
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY not found in .env file")
        # Configure the genai module with the API key
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel('gemini-2.0-flash')  

    def generate_response(self, prompt, context):
        try:
            # Combine context and prompt for the model
            full_prompt = f"{context}\n\nUser Query: {prompt}"
            # Generate response using the model
            response = self.model.generate_content(
                full_prompt,
                generation_config=genai.types.GenerationConfig(
                    max_output_tokens=500
                )
            )
            logging.info(f"Gemini API response received for prompt: {prompt}")
            return response.text
        except Exception as e:
            logging.error(f"Error calling Gemini API: {e}")
            raise

    def process_athlete_data(self, query, athlete_data):
        context = "You are an AI assistant with access to an Olympic athletes database. Provide a concise and natural response based on the following data:\n"
        for athlete in athlete_data:
            context += (f"Name: {athlete['Name']}, Sex: {athlete['Sex']}, Age: {athlete['Age']}, "
                       f"Height: {athlete['Height']} cm, Weight: {athlete['Weight']} kg, "
                       f"Team: {athlete['Team']}, NOC: {athlete['NOC']}, "
                       f"Games: {athlete['Games']}, Year: {athlete['Year']}, Season: {athlete['Season']}, "
                       f"City: {athlete['City']}, Sport: {athlete['Sport']}, Event: {athlete['Event']}, "
                       f"Medal: {athlete['Medal'] if athlete['Medal'] else 'None'}\n")
        return self.generate_response(query, context)