import datetime

class CurrentDateCommand:
    def execute(self):
        now = datetime.datetime.now()
        return now.strftime('%Y-%m-%d')