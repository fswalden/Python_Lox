import lox

class RTError(RuntimeError):
    def __init__(self, token, message):
        #super(message)
        self.message = message
        self.token = token