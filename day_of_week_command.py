import datetime

from base_command import BaseCommand

class DayOfWeekCommand(BaseCommand):
    def __init__(self):
        super().__init__(tag="{WEEKDAY}")

    def execute(self):
        return datetime.datetime.now().strftime('%A')