import mysql.connector 
from dotenv import load_dotenv
import os

class Database:
    def connect(self):
        load_dotenv()  # Load environment variables

        try:
            self.connection = mysql.connector.connect(
                host=os.getenv("DB_HOST"),
                user=os.getenv("DB_USER"),
                password=os.getenv("DB_PASSWORD"),
                database=os.getenv("DB_NAME")
            )
        except mysql.connector.Error as err:
            print(f"Database connection failed: {err}")
            raise
        

    def query(self,query, params=None):
        cursor = self.connection.cursor(dictionary =True)
        if params:
            cursor.execute(query,params)
        else:
            cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()
        return result
    
    def close(self):
        if self.connection.is_connected():
            self.connection.close()
