class VpcNameAlreadyExists(Exception):
    def __init__(self, expression="VpcNameAlreadyExists", message="Vpc already exists!"):
        self.expression = expression
        self.message = message


class VpcNameDoesntExists(Exception):
    def __init__(self, expression="VpcNameDoesntExists", message="Vpc doesn't exists!"):
        self.expression = expression
        self.message = message
