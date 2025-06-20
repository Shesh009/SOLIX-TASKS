import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from Db.db_config import Database

class DBHandler:
    def __init__(self):
        self.db = Database()

    def create_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS QUERY_RESPONSE (
            id SERIAL PRIMARY KEY,
            query TEXT NOT NULL,
            response TEXT NOT NULL,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
        self.db.execute(query)

    def insert_data(self, query_text, response_text):
        query = """
        INSERT INTO QUERY_RESPONSE (query, response)
        VALUES (%s, %s)
        """
        self.db.execute(query, (query_text, response_text))

    def get_records(self, limit=10):
        query = """
        SELECT * FROM QUERY_RESPONSE
        ORDER BY timestamp DESC
        LIMIT %s
        """
        return self.db.fetch_all(query, (limit,))
