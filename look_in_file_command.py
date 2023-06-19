import os

from base_command import BaseCommand

class LookInFileCommand(BaseCommand):
    def __init__(self):
        pass

    def execute(self, params):
        if not os.path.exists(params):
            return f'Error: The file path you provided does not exist.'

        with open(params, 'r') as file:
            content = file.read()

        return content