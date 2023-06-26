import shutil
from commands.base_command import BaseCommand

class CommandMoveFile(BaseCommand):
    def __init__(self):
        self.name = 'move_file'
        self.metadata = {
            'name': self.name,
            'description': 'Move a file from one location to another',
            'parameters': {
                'type': 'object',
                'properties': {
                    'source_path': {
                        'type': 'string',
                        'description': 'The path to the file to be moved',
                    },
                    'destination_path': {
                        'type': 'string',
                        'description': 'The destination path for the file',
                    },
                },
                'required': ['source_path', 'destination_path'],
            },
        }

        super().__init__(self.name, self.metadata)

    def execute(self, source_path, destination_path):
        shutil.move(source_path, destination_path)
        return f'The file has been successfully moved from {source_path} to {destination_path}'