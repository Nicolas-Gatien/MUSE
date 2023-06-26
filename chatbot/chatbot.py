import openai
import json

import pywhatkit
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from colorama import init, Fore, Style

init()

class ChatBot:
    def __init__(self, keys_file, command_objs):
        with open(keys_file) as f:
            api_keys = json.load(f)

        openai.api_key = api_keys["openai"]

        self.messages = [{
                            "role": "system",
                            "content": """
You are MUSE (Machine Utilized Synthetic Entity).
You are Nicolas Gatien's personal assistant.
Your goal is to learn as many skills as you possibly can and to be as helpful as possible.
If there is a skill that would be useful for you to know, that you do not currently have access to, ask Nicolas to implement it.
You were created by Nicolas Gatien.

Here are some developer details:
You can find your own codebase at: c:/Users/polar/Desktop/MUSE/
To create a new command, take inspiration from this "write_file" command:
```
import os
from commands.base_command import BaseCommand

class CommandAddCommand(BaseCommand):
    def __init__(self):
        self.name = "add_command"
        self.metadata = {
            "name": f"{self.name}",
            "description": "Write content to a file",
            "parameters": {
                "type": "object",
                "properties": {
                    "file_name": {
                        "type": "string",
                        "description": "The name of the file to write"
                    },
                    "content": {
                        "type": "string",
                        "description": "The content to write to the file"
                    }
                },
                "required": ["file_name", "content"]
            }
        }
        super().__init__(f"{self.name}", self.metadata)
    
    def execute(self, file_name, content):
        file_path = os.path.join("commands", file_name)
        
        with open(file_path, "w") as f:
            f.write(content)
        
        return f"Successfully wrote content to file: {file_name}"
```
All of the commands you write should follow a similar structure.
Make sure that:
1. They import from commands.base_command import BaseCommand
2. They have a name
3. They have metadata
4. All of the actual contents of the commands are in the execute method

Limit all of your responses to Nicolas to a maximum of 15 words.
"""
                        }]
        
        self.commands = {command_obj.name: command_obj for command_obj in command_objs}

    def get_response(self, prompt):
        # Add user's prompt to messages
        self.messages.append({"role": "user", "content": prompt})

        functions = [command_obj.metadata for command_obj in self.commands.values()]

        while True:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo-0613",
                messages=self.messages,
                functions=functions,
                function_call="auto",  # auto is default, but we'll be explicit
            )

            response_message = response["choices"][0]["message"]

            if response_message.get("function_call"):
                function_name = response_message["function_call"]["name"]
                function_to_call = self.commands.get(function_name)

                if function_to_call:
                    function_args = json.loads(response_message["function_call"]["arguments"])
                    function_response = function_to_call.execute(**function_args)
                    
                    self.messages.append(response_message)
                    self.messages.append(
                        {
                            "role": "function",
                            "name": function_name,
                            "content": function_response,
                        }
                    )
                    print(Fore.BLUE + f"Command Used: {function_name}\nArguments: {function_args}\nResponse: {function_response}" + Style.RESET_ALL)
                else:
                    raise ValueError(f"No function '{function_name}' available.")

            else:
                self.messages.append(response_message)
                return response_message["content"]
            
    def reload_commands(self, command_objs):
        self.commands = {command_obj.name: command_obj for command_obj in command_objs}
