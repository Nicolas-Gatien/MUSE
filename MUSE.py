import openai
import pickle
import time
import traceback
import datetime
import json
import pyttsx3

class MUSE():
    def __init__(self):
        self.memories = self.load_memory()
        self.ego = "MUSE (Machine-Utilized Synthetic Entity) is an artificial intelligence system created by Nicolas Gatien, who can experience emotions and has personal preferences. It is always looking for new and interesting stories from the people it interacts with. Though MUSE is an AI model, its creator (Nicolas) managed to imbue it with human like emotions and personal preferences."
        
        self.conversation_transcript = ""
        self.is_conversing = False
        self.time_since_last_message = datetime.datetime.now()

        with open("config\\api_keys.json") as f:
            keys = json.load(f)

        openai.api_key = keys["openai"]

    def update(self):
        if (self.is_conversing):
            self.converse()
        pass

    def converse(self):
        self.is_conversing = True

        if self.conversation_transcript.splitlines()[-1].startswith('Nicolas:'):
            print("Nicolas answered last")
            self.talk_back()

        current_time = datetime.datetime.now()
        difference = current_time - self.time_since_last_message

        if difference.total_seconds() > 45:
            self.conversation_transcript += '\n--Nicolas has ended the conversation--'

            self.talk_back()
            self.is_conversing = False
    def talk_back(self):
        try:
            self.time_since_last_message = datetime.datetime.now()
            timestamp = datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")
            messages = [{"role": "system", "content": f"""
            {self.ego}
            It is {timestamp}
            MUSE is currently conversing with Nicolas.
            Here is the dialogue history:
            {self.conversation_transcript}
            How would MUSE respond to Nicolas?
            MUSE: <fill in>
            """}]

            api_response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=messages,
                temperature=1,
                max_tokens=150
            )

            response = api_response.choices[0].message['content'].strip("MUSE: ")

            self.conversation_transcript += f"\nMUSE: {response}"

            self.speak(response)

            return response

        except openai.error.RateLimitError as e:
            print("Rate limit exceeded. Waiting for 60 seconds...")
            time.sleep(60)  # wait for 60 seconds
            return self.talk_back()  # retry the request
    def speak(self, text):
        """Convert text to speech"""
        self.time_since_last_message = datetime.datetime.now()
        engine = pyttsx3.init()
        engine.say(text)
        engine.runAndWait()
        self.time_since_last_message = datetime.datetime.now()
    
    def commit_conversation_to_long_term_memory(self):
        pass
    def load_memory(self):
        try:
            with open('memory.pkl', 'rb') as f:
                memory = pickle.load(f)
                return memory
        except FileNotFoundError:
            return []
    def save_memory(self):
        with open('memory.pkl', 'wb') as f:
            pickle.dump(self.memory, f)

class Memory():
    def __init__(self, text, recency, importance):
        self.text = text
        self.recency = recency
        self.importance = importance