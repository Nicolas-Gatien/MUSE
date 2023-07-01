import importlib
import inspect
import json
import os
import pyttsx3
import speech_recognition as sr
import sys
from chatbot.chatbot import ChatBot
from colorama import init, Fore, Style
from commands.base_command import BaseCommand
from datetime import datetime

sys.path.insert(0, './commands')

def load_command_objects():
    command_files = [f[:-3] for f in os.listdir('./commands') if f.endswith('.py') and f != '__init__.py' and f != 'base_command.py']
    command_objs = []

    for file in command_files:
        if file != "__init__":
            #print(f"Importing module: commands.{file}")
            module = importlib.import_module('commands.' + file)
            for name, obj in inspect.getmembers(module):
                if inspect.isclass(obj) and issubclass(obj, BaseCommand) and obj is not BaseCommand:
                    #print(f"Instantiating class: {name}")
                    command_objs.append(obj())

    return command_objs

init()

def speak(text):
    """Convert text to speech"""
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def listen():
    """Listen to user's voice input"""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print(Fore.LIGHTBLACK_EX + "Listening..." + Style.RESET_ALL)
        audio = r.listen(source)
        try:
            text = r.recognize_google(audio)
            return text
        except:
            return ""

command_objs = load_command_objects()
bot = ChatBot("config\\my_api_keys.json", command_objs)

while True:
    command_objs = load_command_objects()
    bot.reload_commands(command_objs)
    user_input = listen()
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

    if user_input:
        prompt = f"{user_input}"
        print(Fore.WHITE + "User: " + prompt)
        response = bot.get_response(prompt)
        print(Fore.YELLOW + "Bot: " + response)
        speak(response)

