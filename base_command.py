class BaseCommand:
    def __init__(self):
        pass

    def execute(self, params=None):
        raise NotImplementedError