import lox
from scanner import Token

class Expr:
    pass

class Binary(Expr):
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right

class Unary(Expr):
    def __init__(self, operator, right):
        self.operator = operator
        self.right = right

class Literal(Expr):
    def __init__(self, literal):
        self.literal = literal

class Grouping(Expr):
    def __init__(self, expr):
        self.expr = expr