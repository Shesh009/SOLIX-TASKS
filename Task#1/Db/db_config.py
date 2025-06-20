import os
import psycopg2
from psycopg2 import extras
from dotenv import load_dotenv

load_dotenv()

class Database:
    def __init__(self):
        self.connection = None
        self.connect()

    def connect(self):
        try:
            self.connection = psycopg2.connect(
                host=os.getenv("DB_HOST"),
                port=os.getenv("DB_PORT"),
                dbname=os.getenv("DB_NAME"),
                user=os.getenv("DB_USER"),
                password=os.getenv("DB_PASSWORD")
            )
            self.connection.autocommit = True
            print("Connected to the database.")
        except Exception as e:
            print("Failed to connect to DB:", e)

    def execute(self, query, params=None):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query, params)
        except Exception as e:
            print("Query execution failed:", e)

    def fetch_all(self, query, params=None):
        try:
            with self.connection.cursor(cursor_factory=extras.DictCursor) as cursor:
                cursor.execute(query, params)
                return cursor.fetchall()
        except Exception as e:
            print("Fetch failed:", e)
            return []

    def close(self):
        if self.connection:
            self.connection.close()
            print("DB connection closed.")
