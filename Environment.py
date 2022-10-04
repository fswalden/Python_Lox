import lox
import RTError

class environment():
    def __init__(self, env = None):
        self.values = {}
        self.enclosing = env

    def define(self, name, value):
        self.values[name.lexeme] = value
    
    def get(self, name):
        val = self.values.get(name.lexeme)

        if val != None:
            return val
        
        if self.enclosing != None:
            return self.enclosing.get(name)

        raise RTError(name, "Undefined variable '" + str(name.lexeme) + "'.")

    def assign(self, name, value):
        if self.values.get(name.lexeme) != None:
            self.values[name.lexeme] = value
            return

        if self.enclosing != None:
            self.enclosing.assign(name, value)
            return

        raise RTError(name, "Undefined variable '" + str(name.lexeme) + "'.")
