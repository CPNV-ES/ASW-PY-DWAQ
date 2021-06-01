class RtbAlreadyExists(Exception):
    def __init__(self, expression="RtbAlreadyExists", message="Rtb already exists!"):
        self.expression = expression
        self.message = message
