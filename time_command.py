import datetime

from base_command import BaseCommand

class TimeCommand(BaseCommand):
    def __init__(self):
        super().__init__(tag="{TIME}")

    def execute(self):
        return datetime.datetime.now().strftime('%I:%M %p')
