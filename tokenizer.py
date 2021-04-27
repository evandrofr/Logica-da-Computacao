reserved = ["PRINT", "BEGIN", "END"]
PRINT, BEGIN, END = reserved

class Token:
    
    """
    TIPOS DE TOKENS:
    - INT    (123)
    - PLUS   ("+")
    - MINUS  ("-")
    - MULT   ("*")
    - DIV    ("/")
    - OP     ("(")
    - CP     (")")
    - ENTER  ("\n")
    - ENDC   (";")
    - ASSIG  ("=")
    - IDENTIFIER - Utilizado na atribuição de variáveis
    - EOF    (end of file)
    """
    def __init__(self, token_type, token_value):
        self.type = token_type
        self.value = token_value

class Tokenizer:
    def __init__(self, origin):
        self.origin = origin
        self.position = 0
        self.actual = self.selectNext()


    """
    Função que identifica Tokens
    """
    def selectNext(self):
        size = len(self.origin)
        numero = 0
        temp = []
        word = ""

        while self.position < size and self.origin[self.position].isspace() and self.origin[self.position]!="\n":
            self.position+=1

        if self.position == size:
            self.actual = Token("EOF", "end")
            return self.actual

        if self.origin[self.position] == '\n':
            self.actual = Token("ENTER", "\n")
            self.position+=1

            return self.actual


        while self.position < size and self.origin[self.position].isspace():
            self.position += 1

        if self.origin[self.position].isdigit():
            while self.position < size and self.origin[self.position].isdigit():
                temp += [self.origin[self.position]]
                self.position += 1
            for idx, alg in enumerate(temp):
                numero += int(alg)*10**(len(temp) - idx - 1)
            self.actual = Token('INT', numero)

        elif self.origin[self.position].isalpha():
            word += self.origin[self.position]
            self.position += 1
            while self.position < size and (self.origin[self.position].isalpha() or self.origin[self.position].isdigit() or self.origin[self.position]=="_"):
                word += self.origin[self.position]
                self.position += 1

            new_word = word.upper()
            
            if word in reserved:
                self.actual = Token(new_word, new_word)
            else: 
                self.actual = Token("IDENTIFIER", new_word)

        elif self.position < size:
            if self.origin[self.position] == '-':
                self.actual = Token('MINUS', '-')
                self.position += 1
            elif self.origin[self.position] == '+':
                self.actual = Token('PLUS', '+')
                self.position += 1
            elif self.origin[self.position] == '*':
                self.actual = Token('MULT', '*')
                self.position += 1
            elif self.origin[self.position] == '/':
                self.actual = Token('DIV', '/')
                self.position += 1
            elif self.origin[self.position] == '(':
                self.actual = Token('OP', '(')
                self.position += 1
            elif self.origin[self.position] == ')':
                self.actual = Token('CP', ')')
                self.position += 1
            
            elif self.origin[self.position] == '=':
                self.actual = Token("ASSIG", "=")
                self.position += 1
                
            elif self.origin[self.position] == '\n':
                self.actual = Token('ENTER', '\n')
                self.position += 1

            else:
                raise NameError("Token inválido.")

        return self.actual