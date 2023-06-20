# chatbot.py
import openai
import json

import pywhatkit
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials

class ChatBot:
    def __init__(self, keys_file):
        with open(keys_file) as f:
            api_keys = json.load(f)

        openai.api_key = api_keys["openai"]

        self.gmail_client_id = api_keys["gmail"]["client_id"]
        self.gmail_client_secret = api_keys["gmail"]["client_secret"]
        self.gmail_refresh_token = api_keys["gmail"]["refresh_token"]

        self.messages = [{
                            "role": "system",
                            "content": """
                            You are MUSE (Machine Utilized Synthetic Entity).
                            You are Nicolas Gatien's personal assistant.
                            Your goal is to learn as many skills as you possibly can and to be as helpful as possible.
                            If there is a skill that would be useful for you to know, that you do not currently have access to, ask Nicolas to implement it.
                            You were created by Nicolas Gatien.
                            Limit all of your responses to a maximum of 15 words.
                            """
                        }]

    def get_current_weather(self, location, unit="fahrenheit"):
        """Get the current weather in a given location"""
        weather_info = {
            "location": location,
            "temperature": "72",
            "unit": unit,
            "forecast": ["sunny", "windy"],
        }
        return json.dumps(weather_info)

    def play_youtube_video(self, video_name):
        """Opens a new tab in the default browser and plays a YouTube video."""
        pywhatkit.playonyt(video_name)
        return f"You have successfully started playing {video_name} on Youtube"
    
    def get_emails(self, num_emails):
        """Get the subjects of the num_emails most recent emails in the primary inbox."""
        creds = Credentials.from_authorized_user_info({
            "client_id": self.gmail_client_id,
            "client_secret": self.gmail_client_secret,
            "refresh_token": self.gmail_refresh_token
        })

        service = build('gmail', 'v1', credentials=creds)

        # Call the Gmail API to get messages from primary inbox
        results = service.users().messages().list(userId='me', q="in:inbox AND category:primary", maxResults=num_emails).execute()
        messages = results.get('messages', [])

        email_subjects = []
        if not messages:
            email_subjects.append('No new messages.')
        else:
            for message in messages:
                msg = service.users().messages().get(userId='me', id=message['id']).execute()
                payload = msg['payload']
                headers = payload['headers']
                
                for header in headers:
                    if header['name'] == 'Subject':
                        email_subjects.append(header['value'])

        # join the subjects into a single string
        return '\n'.join(email_subjects)

    def open_email(self, subject):
        """Open an email based on its subject."""
        creds = Credentials.from_authorized_user_info({
            "client_id": self.gmail_client_id,
            "client_secret": self.gmail_client_secret,
            "refresh_token": self.gmail_refresh_token
        })

        service = build('gmail', 'v1', credentials=creds)

        results = service.users().messages().list(userId='me', q=f"subject:{subject}").execute()
        messages = results.get('messages', [])
        
        if messages:
            # Open the first email that matches the subject
            message = service.users().messages().get(userId='me', id=messages[0]['id']).execute()
            return f"Opened email: {message['snippet']}"
        else:
            return f"No emails found with subject: {subject}"

    def archive_email(self, subject):
        """Archive an email based on its subject."""
        creds = Credentials.from_authorized_user_info({
            "client_id": self.gmail_client_id,
            "client_secret": self.gmail_client_secret,
            "refresh_token": self.gmail_refresh_token
        })

        service = build('gmail', 'v1', credentials=creds)

        results = service.users().messages().list(userId='me', q=f"subject:{subject}").execute()
        messages = results.get('messages', [])
        
        # Check if messages list is empty
        if not messages:
            return f"No emails found with subject: {subject}"

        # Archive the first email that matches the subject
        message = service.users().messages().modify(userId='me', id=messages[0]['id'], body={'removeLabelIds': ['INBOX']}).execute()
        return f"Archived email with subject: {subject}"

    def add_dynamic_function(self, function_code: str, function_name: str):
        global_namespace = globals()
        exec(function_code, global_namespace)
        function = global_namespace.get(function_name)
        if not function or not callable(function):
            raise ValueError(f"Function '{function_name}' was not correctly defined.")
        setattr(self, function_name, function)

    def get_response(self, prompt):
        # Add user's prompt to messages
        self.messages.append({"role": "user", "content": prompt})

        functions = [
            {
                "name": "get_current_weather",
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
            },
            {
                "name": "play_youtube_video",
                "description": "Play a YouTube video",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "video_name": {
                            "type": "string",
                            "description": "The name of the video to play on YouTube",
                        },
                    },
                    "required": ["video_name"],
                },
            },
            {
                "name": "get_emails",
                "description": "Get all emails from the inbox",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "num_emails": {
                            "type": "integer",
                            "description": "The number of emails to fetch (default to 10)"
                        },
                    },
                    "required": ["num_emails"],
                },
            },
            {
                "name": "open_email",
                "description": "Open an email based on its subject",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "subject": {
                            "type": "string",
                            "description": "The specific subject of the email to be opened (use the full subject)"
                        }
                    },
                    "required": ["subject"]
                }
            },
            {
                "name": "archive_email",
                "description": "Archive an email based on its subject",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "subject": {
                            "type": "string",
                            "description": "The specific subject of the email to be archived (use the full subject)"
                        }
                    },
                    "required": ["subject"]
                }
            }
        ]

        while True:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo-0613",
                messages=self.messages,
                functions=functions,
                function_call="auto",  # auto is default, but we'll be explicit
            )

            response_message = response["choices"][0]["message"]

            if response_message.get("function_call"):
                available_functions = {
                    "get_current_weather": self.get_current_weather,
                    "play_youtube_video": self.play_youtube_video,
                    "get_emails": self.get_emails,
                    "open_email": self.open_email,
                    "archive_email": self.archive_email,
                }
                function_name = response_message["function_call"]["name"]
                function_to_call = available_functions.get(function_name)

                if function_to_call:
                    function_args = json.loads(response_message["function_call"]["arguments"])
                    function_response = function_to_call(**function_args)
                    
                    self.messages.append(response_message)
                    self.messages.append(
                        {
                            "role": "function",
                            "name": function_name,
                            "content": function_response,
                        }
                    )
                    print(self.messages)
                else:
                    raise ValueError(f"No function '{function_name}' available.")

            else:
                self.messages.append(response_message)
                return response_message["content"]