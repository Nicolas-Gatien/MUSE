from chatbot import ChatBot
from termcolor import colored

from day_of_week_command import DayOfWeekCommand
from look_in_file_command import LookInFileCommand
from look_in_directory_command import LookInDirectoryCommand

import json
import traceback

muse_context = """
You are MUSE (Machine-Utilized Synthetic Entity).
You are Nicolas Gatien's personal assistant.
Your aim is to be as helpful as possible.

Nicolas Gatien has created multiple entities to help you with your tasks, you can directly address them by appending their tag at the beginning of your response.
Currently, the network of entities consists of:

[ACE] - Is a command writer and executor. [ACE] has access to commands like time of day, setting timers, etc...

Format your response in JSON:
{
"from": "your name",
"to": "tag associated with the entity you are messaging",
"message": "your message"
}

For example, you want to message [ACE] it should look like:
Format your response in JSON:
{
"from": "[MUSE]",
"to": "[ACE]",
"message": "{YOUR MESSAGE}"
}

For example, you want to message [NICOLAS] it should look like:
Format your response in JSON:
{
"from": "[MUSE]",
"to": "[NICOLAS]",
"message": "{YOUR MESSAGE}"
}
"""
MUSE = ChatBot("MUSE", muse_context, "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")

ace_context = """
You are ACE (Automatic Command Executor).
You are MUSE's (Machine-Utilized Synthetic Entity) personal command executor.
You were created by Nicolas Gatien.

Format your response in JSON:
{
"from": "[ACE]",
"to": "[MUSE]",
"message": "your message"
}

For example, you want to message [MUSE] it should look like:
{
"from": "[ACE]",
"to": "[MUSE]",
"message": "{YOUR MESSAGE}"
}

You currently have access to the following commands:
- DayOfWeekCommand().execute() will return which day of the week it is.
- LookInDirectoryCommand().execute(r{path_to_directory}) will return the file structure of the directory.
- LookInFileCommand().executre(r{path_to_file}) will return the contents of the specified file.

To execute commands, add a "commands" section to the JSON and send it to [EXEC]. 
For example, if you want to execute the DayOfWeek command, your response should look like:
{
"from": "[ACE]",
"to": "[EXEC]",
"message": "{YOUR MESSAGE}",
"commands": "DayOfWeekCommand().execute()"
}

If you want to execute the LookInPathCommand command to search the Desktop, your response should look like:
{
"from": "[ACE]",
"to": "[EXEC]",
"message": "{YOUR MESSAGE}",
"commands": " LookInDirectoryCommand().execute(r"C:\\Users\\polar\\Desktop")"
}
>>>
"""
ACE = ChatBot("[ACE]", ace_context, "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")

chatbots = [MUSE, ACE]

def converse(initial_prompt):
    try:
        chatbot = MUSE
        prompt = initial_prompt
        while True:
            response = chatbot.get_response(prompt)
            try:
                response_obj = json.loads(response)  # assuming there's only one response in the list
            except json.JSONDecodeError:
                print("Invalid JSON response received. Ignoring and continuing...")
                print("----------------------------------------------------\n" + response + "\n----------------------------------------------------")
                continue        
            from_agent = response_obj["from"]
            to_agent = response_obj["to"]
            message = response_obj["message"]
            
            # Determine the color based on the "to" field
            if from_agent == "[ACE]":
                print_color = 'yellow'
            elif from_agent == "[MUSE]":
                print_color = 'blue'
            elif from_agent == "[NICOLAS]":
                print_color = 'white'
            else:
                print_color = 'red'  # default to red if there's an unknown recipient
            
            # Print the response
            print(colored(f"FROM: {from_agent} TO: {to_agent}\n{message}", print_color))
            
            # Determine the next chatbot and prompt
            if to_agent == "[ACE]":
                chatbot = ACE
                prompt = response
            elif to_agent == "[MUSE]":
                chatbot = MUSE
                prompt = response
            elif to_agent == "[EXEC]":
                script = response_obj["commands"]
                print(script)
                prompt =f"""
                {{
                "from": "[EXEC]",
                "to": "{chatbot.name}",
                "message": "{eval(script)}"
                }}
                """
                print(prompt)
            elif to_agent == "[NICOLAS]":
                # Take input from the terminal
                prompt = input("[NICOLAS]: ")
                chatbot.chat_history.append({
                    "role": "user",
                    "content": f"[NICOLAS]: {prompt}\n"
                })
            
            # Add the response to the chat history of all other chatbots
            for bot in chatbots:
                if bot != chatbot:
                    bot.chat_history.append({
                        "role": "user",
                        "content": f"{response}\n"
                    })
    except Exception as e:
        error_message = traceback.format_exc()
        with open("error.txt", "a") as error_file:
            error_file.write(f"An error occurred: {str(e)}\n")
            error_file.write(f"Traceback:\n{error_message}\n")
        print(f"An error occurred and has been written to error.txt. Error: {str(e)}")

initial_prompt = "Do you understand? If so, explain what I just explained to you."
converse(initial_prompt)
