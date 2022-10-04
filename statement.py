import lox
from scanner import Token
from abc import ABC, abstractmethod

class Stmt:
    class Visitor(ABC):
        
        @abstractmethod
        def visitBlockStmt(self, stmt):
            pass

        @abstractmethod
        def visitClassStmt(self, stmt):
            pass

        @abstractmethod
        def visitExpressionStmt(self, stmt):
            pass

        @abstractmethod
        def visitFunctionStmt(self, stmt):
            pass

        @abstractmethod
        def visitIfStmt(self, stmt):
            pass

        @abstractmethod
        def visitPrintStmt(self, stmt):
            pass

        @abstractmethod
        def visitReturnStmt(self, stmt):
            pass
        
        @abstractmethod
        def visitVarStmt(self, stmt):
            pass

        @abstractmethod
        def visitWhileStmt(self, stmt):
            pass


class Block(Stmt):
    def __init__(self, statements):
        self.statements = statements
    def accept(self, visitor):
        return visitor.visitBlockStmt(self)


class Class(Stmt):
    def __init__(self, name, superclass, methods):
        self.name = name
        self.superclass = superclass
        self.methods = methods

    def accept(self, visitor):
        return visitor.visitClassStmt(self)

class Expression(Stmt):
    def __init__(self, expression):
        self.expression = expression
    def accept(self, visitor):
        return visitor.visitExpressionStm(self)

class Function(Stmt):
    def __init__(self, name, params, body):
        self.name = name
        self.params = params
        self.body = body
    def accept(self, visitor):
        return visitor.visitFunctionStmt(self)

class If(Stmt):
    def __init__(self, condition, thenBranch, elseBranch):
        self.condition = condition
        self.thenBranch = thenBranch
        self.elseBranch = elseBranch
    def accept(self, visitor):
        return visitor.visitIfStmt(self)

class Print(Stmt):
    def __init__(self, expression):
        self.expression = expression
    def accept(self, visitor):
        return visitor.visitPrintStmt(self)

class Return(Stmt):
    def __init__(self, keyword, value):
        self.keyword = keyword
        self.value = value
    def accept(self, visitor):
        return visitor.visitReturnStmt(self)

class Var(Stmt):
    def __init__(self, name, initializer):
        self.name = name
        self.initializer = initializer
    def accept(self, visitor):
        return visitor.visitVarStmt(self)

class While(Stmt):
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body
    def accept(self, visitor):
        return visitor.visitWhileStmt(self)
