from lib2to3.pgen2.parse import ParseError
import lox
from scanner import TokenType
from scanner import Token
from expr import Binary, Unary, Literal, Grouping

class Parser:
    class ParseError:
        def __init__(RuntimeException):
            pass

    def __init__(self, tokens = []):
        self.tokens = tokens
        self.current = 0

    def parse(self):
        try:
            return self.expression()
        except(ParseError):
            return None

    def expression(self):
        return self.equality()

    def equality(self):
        ex = self.comparison()

        while self.match([TokenType.BANG_EQUAL, TokenType.EQUAL_EQUAL]):
            operator = self.previous()
            right = self.comparison()
            ex = Binary(ex, operator, right)
        return ex

    def match(self, types):
        for type in types:
            if self.check(type):
                self.advance()
                return True
        
        return False

    def check(self, type):
        if self.isAtEnd():
            return False
        return self.peek().type == type

    def advance(self):
        if not self.isAtEnd():
            self.current += 1
        return self.previous()

    def isAtEnd(self):
        return self.peek().type == TokenType.EOF

    def peek(self):
        return self.tokens[self.current]
    
    def previous(self):
        return self.tokens[self.current - 1]

    def comparison(self):
        ex = self.term()

        while self.match([TokenType.GREATER, TokenType.GREATER_EQUAL, TokenType.LESS, TokenType.LESS_EQUAL]):
            operator = self.previous()

            right = self.term()

            ex = Binary(ex, operator, right)

        return ex

    def term(self):
        ex = self.factor()

        while self.match([TokenType.MINUS, TokenType.PLUS]):
            operator = self.previous()
            right = self.factor()
            ex = Binary(ex, operator, right)
        
        return ex

    def factor(self):
        ex = self.unary()

        while self.match([TokenType.SLASH, TokenType.STAR]):
            operator = self.previous()
            right = self.unary()
            ex = Binary(ex, operator, right)
        return ex
    
    def unary(self):
        if self.match([TokenType.BANG, TokenType.MINUS]):
            operator = self.previous()
            right = self.unary()
            val = Unary(operator, right)
            return val
        return self.primary()

    def primary(self):
        if self.match([TokenType.FALSE]):
            ex = Literal(False)
            return ex
        
        if self.match([TokenType.TRUE]):
            ex = Literal(True)
            return ex

        if self.match([TokenType.NIL]):
            ex = Literal(None)
            return ex

        if self.match([TokenType.NUMBER, TokenType.STRING]):
            ex = Literal(self.previous().literal)

        if self.match([TokenType.LEFT_PAREN]):
            ex = self.expression()
            self.consume(TokenType.RIGHT_PAREN, "Expect ')' after expression.")
            ex = Grouping(ex)
            return ex
        
        self.error(self.peek(), "Expect expression.")

    def consume(self, type, message):
        if self.check(type):
            return self.advance()

        self.error(self.peek(), message)
    
    def error(token, message):
        lox.Lox.error2(token, message)

    def synchronize(self):
        self.advance()

        while not self.isAtEnd():
            if self.previous().tokenType == TokenType.SEMICOLON:
                return
            
            type = self.peek().tokenType

            if type == TokenType.CLASS:
                pass
            elif type == TokenType.FUN:
                pass
            elif type == TokenType.VAR:
                pass
            elif type == TokenType.FOR:
                pass
            elif type == TokenType.IF:
                pass
            elif type == TokenType.WHILE:
                pass
            elif type == TokenType.PRINT:
                pass
            elif type == TokenType.RETURN:
                return
            self.advance()
    

        

    
