import logging
import os
from src.database.db import Database
from src.api.api import GeminiAPI

# Ensure the logs directory exists
log_dir = 'logs'
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

# Configure logging
logging.basicConfig(
    filename=os.path.join(log_dir, 'main.log'),
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def main():
    db = Database()
    gemini = GeminiAPI()

    try:
        print("Welcome to the Olympic Athletes AI Agent! Type 'exit' to quit.")
        while True:
            user_input = input("Enter your query (e.g., 'Find athletes from USA' or 'Who plays tennis?' or 'Who won Bronze?'): ")
            if user_input.lower() == 'exit':
                break

            if 'from' in user_input.lower():
                team = user_input.split('from')[-1].strip()
                athlete_data = db.get_athletes_by_team(team)
            elif 'play' in user_input.lower() or 'sport' in user_input.lower():
                sport = user_input.split()[-1].strip()
                athlete_data = db.get_athletes_by_sport(sport)
            
            elif 'won' in user_input.lower():
                medal = user_input.split('won')[-1].strip()
                athlete_data = db.get_athletes_by_medal(medal)
            else:
                name = user_input.strip()
                athlete_data = db.get_athlete_by_name(name)

            if not athlete_data:
                print("No athletes found for your query.")
                logging.info(f"No results for query: {user_input}")
                continue

            response = gemini.process_athlete_data(user_input, athlete_data)
            print(f"Response: {response}")
            logging.info(f"User query: {user_input}, Response: {response}")

    except Exception as e:
        logging.error(f"Error in main loop: {e}")
        print(f"An error occurred: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    main()