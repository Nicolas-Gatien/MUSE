import datetime
from base_command import BaseCommand

class DateCommand(BaseCommand):
    def __init__(self):
        super().__init__(tag="{DATE}")

    def execute(self):
        return datetime.datetime.now().strftime('%Y-%m-%d')