import importlib
import inspect
import json
import os
import pyttsx3
import speech_recognition as sr
import sys
from MUSE import MUSE
from colorama import init, Fore, Style
from datetime import datetime
import time
import threading

init()

with open("config\\api_keys.json") as f:
    keys = json.load(f)

openai_api_key = keys["openai"]

def speak(text):
    """Convert text to speech"""
    engine = pyttsx3.init()
    text = text[6:]
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

bot = MUSE()

def bot_update():
    while True:
        bot.update()
        time.sleep(0.1)  # avoid busy-waiting; you can adjust this sleep duration

# Create a new thread for bot.update
bot_update_thread = threading.Thread(target=bot_update, daemon=True)
bot_update_thread.start()

while True:
    user_input = listen()
    if user_input:
        prompt = f"{user_input}"
        print(Fore.WHITE + "User: " + prompt)
        bot.conversation_transcript += f"\nNicolas: {prompt}"
        bot.is_conversing = True
        print(bot.conversation_transcript)


