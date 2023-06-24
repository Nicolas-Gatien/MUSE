import json
from .base_command import BaseCommand

class CommandGetCurrentWeather(BaseCommand):
    def __init__(self):
        self.name = "get_current_weather"
        self.metadata = {
                "name": f"{self.name}",
                "description": "Get the current weather in a given location",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "location": {
                            "type": "string",
                            "description": "The city and state, e.g. San Francisco, CA",
                        },
                        "unit": {"type": "string", "enum": ["celsius", "fahrenheit"]},
                    },
                    "required": ["location"],
                },
            }
        
        super().__init__(f"{self.name}", self.metadata)

    def execute(self, location, unit="fahrenheit"):
        """Get the current weather in a given location"""
        weather_info = {
            "location": location,
            "temperature": "72",
            "unit": unit,
            "forecast": ["sunny", "windy"],
        }
        return json.dumps(weather_info)
