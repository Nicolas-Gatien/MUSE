import os

from base_command import BaseCommand

class LookInDirectoryCommand(BaseCommand):
    def __init__(self):
        pass

    def execute(self, params):
        if not os.path.exists(params):
            return "That is not a valid path"
        
        directory = os.listdir()
        output = ""
        for dir in directory:
            output += dir
            output += "\n"

        return output