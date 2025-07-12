import mysql.connector
from dotenv import load_dotenv
import os


class Database:
    def __init__(self):
        load_dotenv()  # Load environment variables
        self.connection = None
        self.connect()

    def connect(self):
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

    def get_schema_info_with_comments(self):
        cursor = self.connection.cursor()


        schema_info = {}
        cursor.execute("SHOW TABLES")
        tables = [table[0] for table in cursor.fetchall()]

        for table in tables:
            cursor.execute(f"SHOW FULL COLUMNS FROM {table}")
            columns = []
            for col in cursor.fetchall():
                columns.append({
                    "name": col[0],  # Field
                    "type": col[1],  # Type
                    "description": col[8] if col[8] else ""  # Comment
                })
            schema_info[table] = columns

        return schema_info


    def query(self, query, params=None, max_rows=20):
        cursor = self.connection.cursor(dictionary=True)

        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)

        result = cursor.fetchall()
        cursor.close()

        return result[:max_rows]

    def close(self):
        if self.connection and self.connection.is_connected():
            self.connection.close()
