class RtbAlreadyExists(Exception):
    def __init__(self, expression="RtbAlreadyExists", message="Rtb already exists!"):
        self.expression = expression
        self.message = message


class RtbDoesntExists(Exception):
    def __init__(self, expression="RtbDoesntExists", message="Rtb Doesnt exists!"):
        self.expression = expression
        self.message = message
