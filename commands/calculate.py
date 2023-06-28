import os
from commands.base_command import BaseCommand

class CommandCalculate(BaseCommand):
    def __init__(self):
        self.name = 'calculate'
        self.metadata = {
            'name': self.name,
            'description': 'Calculate the sum, difference, or product of two numbers',
            'parameters': {
                'type': 'object',
                'properties': {
                    'number1': {
                        'type': 'number',
                        'description': 'The first number'
                    },
                    'number2': {
                        'type': 'number',
                        'description': 'The second number'
                    },
                    'operation': {
                        'type': 'string',
                        'enum': ['sum', 'difference', 'product'],
                        'description': 'The operation to perform on the numbers'
                    }
                },
                'required': ['number1', 'number2', 'operation']
            }
        }
        super().__init__(self.name, self.metadata)

    def execute(self, number1, number2, operation):
        if operation == 'sum':
            result = number1 + number2
        elif operation == 'difference':
            result = number1 - number2
        elif operation == 'product':
            result = number1 * number2
        return f'{operation.capitalize()} of {number1} and {number2} is: {result}'
