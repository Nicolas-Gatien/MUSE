import os
from commands.base_command import BaseCommand

class CommandOpenFile(BaseCommand):
    def __init__(self):
        self.name = "open_file"
        self.metadata = {
            "name": self.name,
            "description": "Read and return the contents of a file",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "The path to the file to read",
                    },
                },
                "required": ["path"],
            },
        }

        super().__init__(self.name, self.metadata)



    def execute(self, path):
        """Reads and returns the contents of a file."""
        if os.path.isfile(path):
            with open(path, 'r') as f:
                content = f.read()
            return f"Contents of the file {path}:\n{content}"
        else:
            return f"{path} is not a valid file."
