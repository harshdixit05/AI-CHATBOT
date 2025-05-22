import mysql.connector
import logging
from mysql.connector import Error

# Configure logging
logging.basicConfig(
    filename='logs/database.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class Database:
    def __init__(self):
        self.connection = None
        self.connect()

    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                host='localhost',  
                user='root',       
                password='1234',  
                database='trent'  
            )
            if self.connection.is_connected():
                logging.info("Successfully connected to MySQL database 'trent'")
        except Error as e:
            logging.error(f"Error connecting to MySQL database: {e}")
            raise

    def query(self, query, params=None):
        try:
            cursor = self.connection.cursor(dictionary=True)
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            results = cursor.fetchall()
            cursor.close()
            logging.info(f"Query executed successfully: {query}")
            return results
        except Error as e:
            logging.error(f"Error executing query: {e}")
            raise

    def close(self):
        """Close the database connection."""
        if self.connection and self.connection.is_connected():
            self.connection.close()
            logging.info("Database connection closed")

    def get_athlete_by_name(self, name):
        query = "SELECT * FROM athletes_ WHERE Name LIKE %s"
        return self.query(query, (f"%{name}%",))

    def get_athletes__by_team(self, team):
        query = "SELECT * FROM athletes_ WHERE Team = %s"
        return self.query(query, (team,))

    def get_athletes__by_sport(self, sport):
        query = "SELECT * FROM athletes_ WHERE Sport = %s"
        return self.query(query, (sport,))

    def get_athletes__by_medal(self, medal):
        query = "SELECT * FROM athletes_ WHERE Medal = %s"
        return self.query(query, (medal,))