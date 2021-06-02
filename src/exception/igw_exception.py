class IgwNameAlreadyExists(Exception):
    def __init__(self, expression="IgwNameAlreadyExists", message="Igw already exists!"):
        self.expression = expression
        self.message = message


class IgwNameDoesNotExist(Exception):
    def __init__(self, expression="IgwNameDoesNotExist", message="Igw doesn't exists!"):
        self.expression = expression
        self.message = message


class IgwAlreadyAttached(Exception):
    def __init__(self, expression="IgwAlreadyAttached", message="Igw is already attached!"):
        self.expression = expression
        self.message = message


class IgwNotAttached(Exception):
    def __init__(self, expression="IgwNotAttached", message="Igw is not attached to a vpc!"):
        self.expression = expression
        self.message = message
