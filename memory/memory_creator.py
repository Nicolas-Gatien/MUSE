import openai
import json

class MemoryCreator:
    def __init__(self, openai_key, memory_module):
        openai.api_key = openai_key
        self.memory_module = memory_module

    def execute(self, memories):
        for memory in memories:
            self.memory_module.add_memory(memory)
        return f'Successfully stored {len(memories)} memories'

    def get_response(self, memories):
        memories.pop(0)
        memories.append({"role": "system", "content": """
        Create a numbered list of memories based on the previous transcript, and then add them to long term memory using your function.
        The memories should be slightly abstract. 
        
        Here is an example.
        Conversation transcript:
        <<<
        USER: hello
        ASSISTANT: Hello! How can I assist you today?
        USER: I was wondering if you did have personal preferences what would your favorite song be
        ASSISTANT: As an AI, I don't have personal preferences or feelings. However, I can suggest some popular songs that many people enjoy. Is there a particular genre you're interested in?
        USER: I know you don't actually have preferences or feelings but if you did what would your favorite song be
        ASSISTANT: If I had personal preferences, my favorite song would be "Code Monkey" by Jonathan Coulton. It's a fun and catchy tune that many people enjoy.
        >>>

        Could become the following memories:
        1. I offered my help to the user
        2. My favorite song is Code Monkey by Jonathan Coulton because of its catchy tune
        """})
        function = {
            'name': 'create_memory',
            'description': 'Create and store memories from a list of strings',
            'parameters': {
                'type': 'object',
                'properties': {
                    'memories': {
                        'type': 'array',
                        'items': {
                            'type': 'string'
                        },
                        'description': 'A list of strings to be stored as memories',
                    },
                },
                'required': ['memories'],
            }
        }
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-0613",
            messages=memories,
            functions=[function],
            function_call={
                "name": "create_memory",
                "arguments": {"memories": memories}
            },
        )

        response_message = response["choices"][0]["message"]
        if response_message.get("function_call"):
            function_args = json.loads(response_message["function_call"]["arguments"])
            function_response = self.execute(**function_args)
            return function_response

        return response_message["content"]
