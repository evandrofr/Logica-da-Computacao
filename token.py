class Token:
    def __init__(self, token_type, token_value):
        self.type = token_type
        self.value = token_value

"""
TIPOS DE TOKENS:
 - INT
 - PLUS
 - MINUS
 - EOF (end of file)
"""

class Tokenizer:
    def __init__(self, origin):
        self.origin = origin
        self.position = 0
        self.actual = self.selectNext()

    def selectNext(self):
        size = len(self.origin)
        numero = 0
        temp = []
        while self.position < size and self.origin[self.position].isspace():
            self.position += 1
        if self.position == size:
            self.actual = Token('EOF', 'end')
        elif self.origin[self.position].isdigit():
            while self.position < size and self.origin[self.position].isdigit():
                temp += [self.origin[self.position]]
                self.position += 1
            for idx, alg in enumerate(temp):
                numero += int(alg)*10**(len(temp) - idx - 1)
            self.actual = Token('INT', numero)
        elif self.position < size:
            if self.origin[self.position] == '-':
                self.actual = Token('MINUS', '-')
                self.position += 1
            if self.origin[self.position] == '+':
                self.actual = Token('PLUS', '+')
                self.position += 1
        return self.actual

class Parser:
    def parserExpression():
        if Parser.tokenizer.actual.type == 'INT':
            print(Parser.tokenizer.actual.type, Parser.tokenizer.actual.value, "\n")
            resultado = Parser.tokenizer.actual.value
            Parser.tokenizer.selectNext()
            print(Parser.tokenizer.actual.type, Parser.tokenizer.actual.value, "\n")
            while Parser.tokenizer.actual.type == 'PLUS' or Parser.tokenizer.actual.type == 'MINUS':
                if Parser.tokenizer.actual.type == 'PLUS':
                    Parser.tokenizer.selectNext()
                    print(Parser.tokenizer.actual.type, Parser.tokenizer.actual.value, "\n")
                    if Parser.tokenizer.actual.type == 'INT':
                        resultado += Parser.tokenizer.actual.value
                    else:
                        print("Erro")
                elif Parser.tokenizer.actual.type == 'MINUS':
                    Parser.tokenizer.selectNext()
                    print(Parser.tokenizer.actual.type, Parser.tokenizer.actual.value, "\n")
                    if Parser.tokenizer.actual.type == 'INT':
                        resultado -= Parser.tokenizer.actual.value
                    else:
                        print("Erro")
                Parser.tokenizer.selectNext()
                print(Parser.tokenizer.actual.type, Parser.tokenizer.actual.value, "\n")
        return resultado
    
    def run(code):
        Parser.tokenizer = Tokenizer(code)
        return Parser.parserExpression()

print(Parser.run("1  +2 + 3-  1 -  2    -   3    +               1"))