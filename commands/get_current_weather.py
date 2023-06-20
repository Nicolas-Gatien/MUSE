import json

def get_current_weather(self, location, unit="fahrenheit"):
        """Get the current weather in a given location"""
        weather_info = {
            "location": location,
            "temperature": "72",
            "unit": unit,
            "forecast": ["sunny", "windy"],
        }
        return json.dumps(weather_info)