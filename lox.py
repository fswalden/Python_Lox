import sys
from CS503.Interpreter.Lox.scanner import TokenType
import scanner
import parser
import interpreter

args = sys.argv

class Lox:
    def __init__(self):
        self.hadError = False
        self.hadRuntimeError = False
        self.interprety = interpreter.Interpreter()
    def runFile(self, path):
        f = open(path, 'r')
        data = f.read()
        f.close
        if self.hadError:
            sys.exit(65)
        if self.hadRuntimeError:
            sys.exit(70)
        self.run(data)

    def runPrompt(self):
        while True:
            data = None
            try:
                data = input('> ')
            except EOFError:
                break
            
            self.run(data)
            self.hadError = False
    
    def run(self, source):
        scanny = scanner.Scanner(source)
        tokens = scanny.scanTokens()
        
        parsy = parser.Parser(tokens)

        statements = parsy.parse()

        if self.hadError:
            return
        if self.hadRuntimeError:
            return
        self.interprety.interpret(statements)
        #AstPrinty = Tool.GenerateAst.
        
    
    def error(self, line, message):
        self.report(line, "", message)

    def error2(self, token, message):
        if token.tokenType == TokenType.EOF:
            self.report(token.line, " at end", message)
        else:
            self.report(token.line, " at '" + token.lexeme + "'", message)
    
    def runtimeError(self, err):
        print(err.message +
        "\n[line " + str(err.token.line) + "]")
        self.hadRuntimeError = True

    def report(self, line, where, message):
        sys.stderr.write("[line " + line + "] Error" + where + ": " + message)
        self.hadError = True

loxy = Lox()
if __name__ == '__main__':
    #print(len(args))
    if len(args) > 2:
        sys.exit(64)
    elif len(args) == 2:
        loxy.runFile(str(args[1]))
    else:
        loxy.runPrompt()


