import datetime

from base_command import BaseCommand

class DayOfWeekCommand(BaseCommand):
    def __init__(self):
        pass

    def execute(self):
        return datetime.datetime.now().strftime('%A')