import os
from .base_command import BaseCommand

class CommandListFilesAndDirectories(BaseCommand):
    def __init__(self):
        self.name = "list_files_and_directories"
        self.metadata = {
            "name": self.name,
            "description": "List all the files and directories in a given path",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "The path to the directory to list files and directories from",
                    },
                },
                "required": ["path"],
            },
        }

        super().__init__(self.name, self.metadata)

    def execute(self, path):
        """Lists all the files and directories in a given path."""
        if not os.path.isdir(path):
            path_doc = os.path.join(os.path.expanduser('~'), 'Documents')  # get the documents directory path
            return f"{path} is not a valid directory. Here is the path to the Documents folder instead:\n{path_doc}"

        content = os.listdir(path)
        return f"Contents of the directory {path}:\n{' '.join(content)}"
