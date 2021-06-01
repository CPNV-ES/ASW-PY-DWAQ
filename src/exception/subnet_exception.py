class SubnetNameAlreadyExists(Exception):
    def __init__(self, expression="SubnetNameAlreadyExists", message="Subnet already exists!"):
        self.expression = expression
        self.message = message


class SubnetNameDoesntExists(Exception):
    def __init__(self, expression="SubnetNameDoesntExists", message="Subnet doesn't exists!"):
        self.expression = expression
        self.message = message


class SubnetCidrBlockException(Exception):
    def __init__(self, expression="SubnetCidrBlockException", message="Cidr block error!"):
        self.expression = expression
        self.message = message
