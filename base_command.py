import re

class BaseCommand:
    def __init__(self, tag):
        self.tag = tag

    def check_tag(self, text):
        return bool(re.search(r'{}(:\w+)?'.format(self.tag), text))

    def execute(self, params=None):
        raise NotImplementedError
