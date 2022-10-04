import lox
from expr import *
from scanner import *
from RTError import RTError
from statement import *
from Environment import *

loxy = lox.Lox

class Interpreter(Expr.Visitor, Stmt.Visitor):

    def __init__(self):
        self.environmenty = environment()
    def interpret(self, statements):
        try:
            for statement in statements:
                self.execute(statement)
        except RTError:
            loxy.runtimeError(RTError)


    def visitLiteralExpr(self, expr):
        return expr.value
    
    def visitGroupingExpr(self, expr):
        return self.evaluate(expr.expression)

    def evaluate(self, expr):
        return expr.accept(self)

    def execute(self, stmt):
        return stmt.accept(self)

    def executeBlock(self, statements, envy):
        previous = self.environmenty
        try:
            self.environmenty = envy
            for statement in statements:
                self.execute(statement)
        finally:
            self.environmenty = previous

    def visitBlockStmt(self, stmt):
        envy = environment(self.environmenty)
        self.executeBlock(stmt.statements, envy)
        return None

    def visitExpressionStmt(self, stmt):
        self.evaluate(stmt.expression)
        return None
    
    def visitPrintStmt(self, stmt):
        value = self.evaluate(stmt.expression)
        print(self.stringifiy(value))
        return None

    def visitVarStmt(self, stmt):
        value = None
        if stmt.initalizer != None:
            value = self.evaluate(stmt.initializer)

        self.environmenty.define(stmt.name.lexeme, value)
        return None

    def visitAssignExpr(self, expr):
        value = self.evaluate(expr.value)
        self.environmenty.assign(expr.name, value)
        return value

    def visitUnaryExpr(self, expr):
        right = self.evaluate(expr.right)

        if expr.operator.type == TokenType.BANG:
            return not self.isTruthy(right)
        elif expr.operator.type == TokenType.MINUS:
            self.checkNumberOperand(expr.operator, right)
            return (float(right)) * -1

        return None
    
    def visitVariableExpr(self, expr):
        return self.environmenty.get(expr.name)

    def isTruthy(self, object):
        if object == None:
            return False
        if type(object) == bool:
            return bool(object)

        return True

    def isEqual(self, a, b):
        if a == None and b == None:
            return True
        if a == None:
            return False
        return a == b

    def stringifiy(self, object):
        if object == None:
            return 'nil'
        if type(object) == float:
            text = str(object)
            if text[-2:] == '.0':
                text = text[:-2]
            return text
        return str(object)

    def visitBinaryExpr(self, expr):
        left = self.evaluate(expr.left)
        right = self.evaluate(expr.right)

        if expr.operator.type == TokenType.MINUS:
            self.checkNumberOperands(expr.operator, left, right)
            return float(left) - float(right)
        elif expr.operator.type == TokenType.SLASH:
            self.checkNumberOperands(expr.operator, left, right)
            return float(left) / float(right)
        elif expr.operator.type == TokenType.STAR:
            self.checkNumberOperands(expr.operator, left, right)
            return float(left) * float(right)
        elif expr.operator.type == TokenType.PLUS:
            if type(left) == str and type(right) == str:
                return str(left) + str(right)

            if type(left) == float and type(right) == float:
                return float(left) + float(right)
            raise RTError(expr.operator, "Operands must be two numbers or two strings.")
        elif expr.operator.type == TokenType.GREATER:
            self.checkNumberOperands(expr.operator, left, right)
            return float(left) > float(right)
        elif expr.operator.type == TokenType.GREATER_EQUAL:
            self.checkNumberOperands(expr.operator, left, right)
            return float(left) >= float(right)
        elif expr.operator.type == TokenType.LESS:
            self.checkNumberOperands(expr.operator, left, right)
            return float(left) < float(right)
        elif expr.operator.type == TokenType.LESS_EQUAL:
            self.checkNumberOperands(expr.operator, left, right)
            return float(left) <= float(right)
        elif expr.operator.type == TokenType.BANG_EQUAL:
            return not self.isEqual(left, right)
        elif expr.operator.type == TokenType.EQUAL_EQUAL:
            return self.isEqual(left, right)
        return None
    
    def checkNumberOperand(operator, operand):
        if type(operand) == float:
            return
        raise RTError(operator, "Operand must be a number.")

    def checkNumberOperands(operator, left, right):
        if type(left) == float and type(right) == float:
            return
        raise RTError(operator, "Operands must be numbers")