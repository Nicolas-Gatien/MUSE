import speech_recognition as sr
import pyttsx3
from chatbot.chatbot import ChatBot
from datetime import datetime

import json
from colorama import init, Fore, Style

from commands.archive_email import CommandArchiveEmail
from commands.get_current_weather import CommandGetCurrentWeather
from commands.get_emails import CommandGetEmails
from commands.open_email import CommandOpenEmail
from commands.play_youtube_video import CommandPlayYoutubeVideo
from commands.read_file import CommandReadFile
from commands.list_files_and_directories import CommandListFilesAndDirectories
from commands.write_file import CommandWriteFile


command_objs = [
    CommandOpenEmail(),
    CommandArchiveEmail(),
    CommandGetCurrentWeather(),
    CommandGetEmails(),
    CommandPlayYoutubeVideo(),
    CommandReadFile(),
    CommandListFilesAndDirectories(),
    CommandWriteFile(),
]

init()

with open("config\\api_keys.json") as f:
    keys = json.load(f)

openai_api_key = keys["openai"]

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

bot = ChatBot("config\\api_keys.json", command_objs)

while True:
    user_input = listen()
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

    if user_input:
        prompt = f"{user_input}"
        print(Fore.WHITE + "User: " + prompt)
        response = bot.get_response(prompt)
        print(Fore.YELLOW + "Bot: " + response)
        speak(response)
