from enum import Enum
from multiprocessing import current_process
import lox


class TokenType:
    # Single character tokens
    LEFT_PAREN = 1
    RIGHT_PAREN = 2
    LEFT_BRACE = 3
    RIGHT_BRACE= 4
    COMMA = 5
    DOT = 6
    MINUS = 7
    PLUS = 8
    SEMICOLON = 9
    SLASH = 10
    STAR = 11

    # One or two character tokens.
    BANG = 12
    BANG_EQUAL = 13
    EQUAL = 14
    EQUAL_EQUAL = 15
    GREATER = 16
    GREATER_EQUAL = 17
    LESS = 18
    LESS_EQUAL = 19

    # Literals.
    IDENTIFIER = 20
    STRING = 21
    NUMBER = 22

    # Keywords.
    AND = 23
    CLASS = 24
    ELSE = 25
    FALSE = 26
    FUN = 27
    FOR = 28
    IF = 29
    NIL = 30
    OR = 31
    PRINT = 32
    RETURN = 33
    SUPER = 34
    THIS = 35
    TRUE = 36
    VAR = 37
    WHILE = 38


    EOF = 39
        

class Token:
    def __init__(self, tokenType, lexeme, literal, line):
        self.tokenType = tokenType
        self.lexeme = lexeme
        self.literal = literal
        self.line = line
    def toString(self):
        return (str(self.tokenType) + " " + self.lexeme + " " + str(self.literal))

class Scanner:
    def __init__(self, source):
        self.source = source
        self.tokens = []
        self.start = 0
        self.current = 0
        self.line = 1

        self.keywords = {
            'and': TokenType.AND,
            'class': TokenType.CLASS,
            'else': TokenType.ELSE,
            'false': TokenType.FALSE,
            'for': TokenType.FOR,
            'fun': TokenType.FUN,
            'if': TokenType.IF,
            'nil': TokenType.NIL,
            'or': TokenType.OR,
            'print': TokenType.PRINT,
            'return': TokenType.RETURN,
            'super': TokenType.SUPER,
            'this': TokenType.THIS,
            'true': TokenType.TRUE,
            'var': TokenType.VAR,
            'while': TokenType.WHILE
        }
        
    def scanTokens(self):
        while not self.isAtEnd():
            start = self.current
            self.scanToken()
        t = Token(TokenType.EOF, "", None, self.line)
        self.tokens.append(t)
        return self.tokens
    
    def isAtEnd(self):
        if self.current >= len(self.source):
            return True
        else:
            return False
    def scanToken(self):
        c = self.advance()
        if c == '(':
            self.addToken(TokenType.LEFT_PAREN)
        elif c == ')':
            self.addToken(TokenType.RIGHT_PAREN)
        elif c == '{':
            self.addToken(TokenType.LEFT_BRACE)
        elif c == '}':
            self.addToken(TokenType.RIGHT_BRACE)
        elif c == ',':
            self.addToken(TokenType.COMMA)
        elif c == '.':
            self.addToken(TokenType.DOT)
        elif c == '-':
            self.addToken(TokenType.MINUS)
        elif c == '+':
            self.addToken(TokenType.PLUS)
        elif c == ';':
            self.addToken(TokenType.SEMICOLON)
        elif c == '*':
            self.addToken(TokenType.STAR)
        elif c == '!':
            self.addToken(TokenType.BANG_EQUAL if self.match('=') else TokenType.BANG)
        elif c == '=':
            self.addToken(TokenType.EQUAL_EQUAL if self.match('=') else TokenType.EQUAL)
        elif c == '<':
            self.addToken(TokenType.LESS_EQUAL if self.match('=') else TokenType.LESS)
        elif c == '>':
            self.addToken(TokenType.GREATER_EQUAL if self.match('=') else TokenType.GREATER)
        elif c == '/':
            if self.match('/'):
                while self.peek() != '\n' and not (self.isAtEnd()):
                    self.advance()
            else:
                self.addToken(TokenType.SLASH)
        elif c == ' ':
            pass
        elif c == '\r':
            pass
        elif c == '\t':
            pass
        elif c == '\n':
            self.line += 1
        elif c == '"':
            self.string()
        elif self.isDigit(c):
            self.number()
        elif self.isAlpha(c):
            self.identifier()
        else:
            lox.error(self.line, "Unexpected Character.")
    
    def identifier(self):
        while self.isAlphaNumeric(self.peek()):
            self.advance()
        text = self.source[self.start, self.current]
        type = self.keywords[text]
        if type == None:
            type = TokenType.IDENTIFIER
        self.addToken(type)
        

    def number(self):
        while self.isDigit(self.peek()):
            self.advance()
        if self.peek == '.' and self.isDigit(self.peekNext()):
            self.advance()

            while self.isDigit(self.peek()):
                self.advance()
        
        self.addToken(TokenType.NUMBER, float(self.source[self.start, self.current]))
    
    def string(self):
        while self.peek() != '"' and not (self.isAtEnd()):
            if self.peek() == '\n':
                self.line += 1
            self.advance()
        if self.isAtEnd():
            lox.error(self.line, "Unterminated String.")
            return
        
        self.advance()

        value = self.source((self.start) + 1, (self.current) - 1)
        self.addToken(TokenType.STRING, value)

    def advance(self):
        return self.source[self.current]
        self.current = self.current + 1
    def addToken(self, type):
        self.addToken2(type, None)
    def addToken2(self, type, literal):
        text = self.source[self.start, self.current]
        t = Token(type, text, literal, self.current)
        self.tokens.append(t)
    def match(self, expected):
        if self.isAtEnd():
            return False
        if self.source[self.current] != expected:
            return False
        self.current += self.current
        return True
    def peek(self):
        if self.isAtEnd():
            return '\0'
        return self.source[self.current]

    def peekNext(self):
        if self.current + 1 >= len(self.source):
            return '\0'
        return self.source[self.current + 1]

    def isAlpha(self, c):
        return (c >= 'a' and c <= 'z') or (c >= 'A' and c <= 'Z') or c == '_'

    def isAlphaNumeric(self, c):
        return self.isAlpha(c) or self.isDigit(c)

    def isDigit(self, c):
        return c >= '0' and c <= '9'
    


