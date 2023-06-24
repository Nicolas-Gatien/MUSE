# chatbot.py
import openai
import json

import pywhatkit
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from commands.archive_email import CommandArchiveEmail
from commands.get_current_weather import CommandGetCurrentWeather
from commands.get_emails import CommandGetEmails
from commands.open_email import CommandOpenEmail
from commands.play_youtube_video import CommandPlayYoutubeVideo

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
        
        self.command_open_email = CommandOpenEmail()
        self.command_archive_email = CommandArchiveEmail()
        self.command_get_current_weather = CommandGetCurrentWeather()
        self.command_get_emails = CommandGetEmails()
        self.command_play_youtube_video = CommandPlayYoutubeVideo()

    def get_response(self, prompt):
        # Add user's prompt to messages
        self.messages.append({"role": "user", "content": prompt})

        functions = [
            self.command_open_email.metadata,
            self.command_archive_email.metadata,
            self.command_get_current_weather.metadata,
            self.command_get_emails.metadata,
            self.command_play_youtube_video.metadata
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
                    self.command_open_email.name: self.command_open_email.execute(),
                    self.command_archive_email.name: self.command_archive_email.execute(),
                    self.command_get_current_weather.name: self.command_get_current_weather.execute(),
                    self.command_get_emails.name: self.command_get_emails.execute(),
                    self.command_play_youtube_video.name: self.command_play_youtube_video.execute(),
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