import sys
import scanner

args = sys.argv

class Lox:
    def __init__(self):
        self.hadError = False
    def runFile(self, path):
        f = open(path, 'r')
        data = f.read()
        f.close
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
        prompt = len(args) < 2
        outfile = None
        f = None
        if not prompt:
            outfile = 'out' + (str(args[1]))[4] + '.txt'
            f = open(outfile, 'w')
        for token in tokens:
            if(prompt):
                print("<<" + token.toString() + ">> ")
            else:
                f.write("<<" + token.toString() + ">> \n")
        if not prompt:
            f.close()
    
    def error(self, line, message):
        self.report(line, "", message)
    
    def report(self, line, where, message):
        sys.stderr.write("[line " + line + "] Error" + where + ": " + message)
        self.hadError = True

interpreter = Lox()
if __name__ == '__main__':
    #print(len(args))
    if len(args) > 2:
        sys.exit(64)
    elif len(args) == 2:
        interpreter.runFile(str(args[1]))
    else:
        interpreter.runPrompt()


