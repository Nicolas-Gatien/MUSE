import openai
import traceback
import time

class ChatBot:
    def __init__(self, name, start_context, api_key, model="gpt-4", temperature=1):
        self.name = name
        self.model = model
        self.temperature = temperature
        self.chat_history = [
            {
                "role": "system",
                "content": start_context
            }
        ]
        openai.api_key = api_key

    def get_response(self, prompt):
        self.chat_history.append({
            "role": "user",
            "content": f"""{prompt}"""
        })
        
        try:
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=self.chat_history,
                temperature=self.temperature,
            )

            self.chat_history.append({
                "role": "assistant",
                "content": f"{response.choices[0].message['content']}"
            })
            
            return response.choices[0].message['content']

        except openai.error.RateLimitError as e:
            print("Rate limit exceeded. Waiting for 60 seconds...")
            time.sleep(60)  # wait for 60 seconds
            return self.get_response(prompt)  # retry the request

        except Exception as e:
            error_message = traceback.format_exc()
            with open("error.txt", "a") as error_file:
                error_file.write(f"An error occurred: {str(e)}\n")
                error_file.write(f"Traceback:\n{error_message}\n")
            print(f"An error occurred and has been written to error.txt. Error: {str(e)}")
