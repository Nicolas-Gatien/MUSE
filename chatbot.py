from time_command import TimeCommand
from date_command import DateCommand
from timer_command import TimerCommand
from day_of_week_command import DayOfWeekCommand

import traceback
import openai
import re

class Chatbot:
    def __init__(self, openai_api_key):
        self.openai_api_key = openai_api_key
        self.commands = [TimeCommand(), DateCommand(), TimerCommand(), DayOfWeekCommand()]
        self.chat_history = [
            {
                "role": "system",
                "content": """
                You are MUSE (Machine Utilized Synthetic Entity).
                You are Nicolas Gatien's personal assistant.
                Your goal is to be as helpful as possible.

                In order to help Nicolas, you have access to the following commands:

                {TIME} - will replace the tag with the current timeGreat, 
                {DATE} - will replace the tag with the current date
                {WEEKDAY} - will replace the tag with the current day of the week
                {TIMER:30} - will set a 30 second timer

                If you are in need of a specific command that is not in that list, write a custom implementation.
                This is what the BaseCommand script looks like:
                |||
                class BaseCommand:
                    def __init__(self, tag):
                        self.tag = tag

                    def check_tag(self, text):
                        return self.tag in text

                    def execute(self, params=None):
                        raise NotImplementedError
                |||

                Here is what the TimeCommand script looks like:
                |||
                import datetime

                from base_command import BaseCommand

                class TimeCommand(BaseCommand):
                    def __init__(self):
                        super().__init__(tag="{TIME}")

                    def execute(self):
                        return datetime.datetime.now().strftime('%I:%M %p')
                |||

                Use the information from those scripts to write your own custom command.
                Ask Nicolas to implement the new command and supply him a tag.

                You can use commands by incorperating the tag in your response. 
                Here are some example conversations:
                <<<
                Nicolas: Hey MUSE! What time is it?
                MUSE: Hello Sir, it is currently {TIME}
                >>>

                <<<
                Nicolas: What date is it?
                MUSE: It is {DATE}
                >>>

                <<<
                Nicolas: Set a timer for me real quick
                MUSE: Of course, I have set a 30 second timer {TIMER}
                >>>
                """
            }
        ]

    def get_response(self, prompt, temperature=1):
        self.chat_history.append({
            "role": "user",
            "content": f"""Nicolas: {prompt}"""
        })
        
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=self.chat_history,
            temperature=temperature,
        )

        response.choices[0].message['content'] = self.execute_commands_in_response(response.choices[0].message['content'])
        
        self.chat_history.append({
            "role": "assistant",
            "content": response.choices[0].message['content']
        })
        
        return response.choices[0].message['content']

    def execute_commands_in_response(self, response):
        for command in self.commands:
            if command.check_tag(response):
                param_regex = r'{}:(\w+)'.format(command.tag)
                param_matches = re.findall(param_regex, response)
                if param_matches:
                    for param in param_matches:
                        full_command = f'{command.tag}:{param}'
                        response = response.replace(full_command, command.execute(param))
                else:
                    response = response.replace(command.tag, command.execute())
        return response

    def chat(self):
        openai.api_key = self.openai_api_key
        while True:
            try:
                prompt = input("User: ")
                response = self.get_response(prompt)
                response = self.execute_commands_in_response(response)
                print(f"MUSE: {response}")

            except Exception as e:
                error_message = traceback.format_exc()
                with open("error.txt", "a") as error_file:
                    error_file.write(f"An error occurred: {str(e)}\n")
                    error_file.write(f"Traceback:\n{error_message}\n")
                print(f"An error occurred and has been written to error.txt. Error: {str(e)}")

if __name__ == "__main__":
    chatbot = Chatbot(openai_api_key='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')
    chatbot.chat()