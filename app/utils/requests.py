import requests
import numpy as np

class ATTAPI:
    def __init__(self, url):
        self.url = url

    def llm(self, text: str):
        payload = {"text": text}
        try:
            response = requests.post(self.url + "chat_llm/", json=payload)
            response.raise_for_status()  
            return response.text
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
            return None