# main.py
import speech_recognition as sr
import pyttsx3
from chatbot.chatbot import ChatBot
from datetime import datetime

import json

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
        audio = r.listen(source)
        try:
            text = r.recognize_google(audio)
            return text
        except:
            return ""

bot = ChatBot("config\\api_keys.json")

while True:
    user_input = listen()
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

    if user_input:
        prompt =f"""{user_input}"""
        print("User: ", prompt)
        response = bot.get_response(prompt)
        print("Bot: ", response)
        speak(response)
