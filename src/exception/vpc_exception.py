class VpcNameAlreadyExists(Exception):
    def __init__(self, expression, message):
        self.expression = expression
        self.message = message


class VpcNameDoesntExists(Exception):
    def __init__(self, expression, message):
        self.expression = expression
        self.message = message
