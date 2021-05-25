class SubnetNameAlreadyExists(Exception):
    def __init__(self, expression, message):
        self.expression = expression
        self.message = message


class SubnetNameDoesntExists(Exception):
    def __init__(self, expression, message):
        self.expression = expression
        self.message = message
