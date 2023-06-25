import os
from commands.base_command import BaseCommand

class CommandWriteFile(BaseCommand):
    def __init__(self):
        self.name = "write_file"
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