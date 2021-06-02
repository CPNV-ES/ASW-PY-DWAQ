class VpcNameAlreadyExists(Exception):
    def __init__(self, expression="VpcNameAlreadyExists", message="Vpc already exists!"):
        self.expression = expression
        self.message = message


class VpcNameDoesNotExist(Exception):
    def __init__(self, expression="VpcNameDoesNotExist", message="Vpc doesn't exists!"):
        self.expression = expression
        self.message = message
