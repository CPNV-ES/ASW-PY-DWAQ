class IgwNameAlreadyExists(Exception):
    def __init__(self, expression="IgwNameAlreadyExists", message="Igw already exists!"):
        self.expression = expression
        self.message = message


class IgwNameDoesntExists(Exception):
    def __init__(self, expression="IgwNameDoesntExists", message="Igw doesn't exists!"):
        self.expression = expression
        self.message = message


class IgwAlreadyAttach(Exception):
    def __init__(self, expression="IgwAlreadyAttach", message="Igw is already attached!"):
        self.expression = expression
        self.message = message


class IgwNotAttach(Exception):
    def __init__(self, expression="IgwNotAttach", message="Igw is not attached to a vpc!"):
        self.expression = expression
        self.message = message
