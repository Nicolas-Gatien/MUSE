import json

class BaseCommand():
    def __init__(self, name, metadata):
        with open("config\\my_api_keys.json") as f:
            self.keys = json.load(f)
            self.name = name
            self.metadata = metadata
        
    def get_openai_key(self):
        return self.keys["openai"]
    
    def get_gmail_client_id(self):
        return self.keys["gmail"]["client_id"]
    
    def get_gmail_client_secret(self):
        return self.keys["gmail"]["client_secret"]
    
    def get_gmail_refresh_token(self):
        return self.keys["gmail"]["refresh_token"]
    
    def execute():
        pass