import requests
import os
from dotenv import load_dotenv
load_dotenv()

class BackendHandler:
    def __init__(self):
        self.backend_url = os.getenv("BACKEND_URL")
        if not self.backend_url:
            raise ValueError("BACKEND_URL environment variable is not set.")

    def send_query(self, query):
        url = f"{self.backend_url}"
        headers = {
            'Content-Type': 'application/json'
        }
        data = {
            "query": query,
            "variables": {}
        }
        try:
            response = requests.post(url, headers=headers, json=data)
            if response.status_code == 200:
              return response.json()
            else:
                print(f"Error: Received status code {response.status_code} from backend.")
        except requests.exceptions.RequestException as e:
            print(f"Error sending request to backend: {e}")
        return None