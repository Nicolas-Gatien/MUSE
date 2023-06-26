import os
import wikipedia
from commands.base_command import BaseCommand

class CommandWikipedia(BaseCommand):
    def __init__(self):
        self.name = "wikipedia"
        self.metadata = {
            "name": f"{self.name}",
            "description": "Pull content from a given Wikipedia page",
            "parameters": {
                "type": "object",
                "properties": {
                    "page": {
                        "type": "string",
                        "description": "The page on Wikipedia to pull content from"
                    }
                },
                "required": ["page"]
            }
        }
        super().__init__(f"{self.name}", self.metadata)
    
    def execute(self, page):
        content = wikipedia.summary(page, sentences = 500)
        return content