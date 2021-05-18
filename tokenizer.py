reserved = ["println", "while", "if", "else", "readln", "int", "bool", "string", "true", "false"]
PRINTLN, WHILE, IF, ELSE, READLN, INT, BOOL, STRING, TRUE, FALSE = reserved

class Token:
    
    """
    TIPOS DE TOKENS:
    - INT     (123)
    - STR     (STR)
    - PLUS    ("+")
    - MINUS   ("-")
    - MULT    ("*")
    - DIV     ("/")
    - OP      ("(")
    - CP      (")")
    - OK      ("{")
    - CK      ("}")
    - ENDC    (";")
    - ASSIG   ("=")
    - GREATER (">")
    - LESS    ("<")
    - AND     ("&&")
    - OR      ("||")
    - EQUAL   ("==")
    - NOT     ("!")
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

        while self.position < size and (self.origin[self.position].isspace() or self.origin[self.position] == "\n"):
            self.position += 1

        if self.position == size:
            self.actual = Token("EOF", "end")
            return self.actual

        if self.origin[self.position].isdigit():
            while self.position < size and self.origin[self.position].isdigit():
                temp += [self.origin[self.position]]
                self.position += 1
            if self.origin[self.position].isalpha():
                 raise NameError("Token inválido. Números não podem conter letras e variáveis não podem iniciar com números.")
            for idx, alg in enumerate(temp):
                numero += int(alg)*10**(len(temp) - idx - 1)
            self.actual = Token('INT', numero)

        elif  self.origin[self.position] == '"':
            self.position += 1
            while self.position < size and self.origin[self.position] !='"':
                word += self.origin[self.position]
                self.position += 1
            self.position += 1
            self.actual = Token("STR", word)
        
        elif self.origin[self.position].isalpha():
            word += self.origin[self.position]
            self.position += 1
            while self.position < size and (self.origin[self.position].isalpha() or self.origin[self.position].isdigit() or self.origin[self.position]=="_"):
                word += self.origin[self.position]
                self.position += 1
            
            if word in reserved:
                self.actual = Token(word, word)
            else:
                self.actual = Token("IDENTIFIER", word)

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

            elif self.origin[self.position] == '{':
                self.actual = Token('OK', '{')
                self.position += 1

            elif self.origin[self.position] == '}':
                self.actual = Token('CK', '}')
                self.position += 1

            elif(self.origin[self.position] == '=' and self.origin[self.position + 1] == "="):
                self.actual = Token("EQUAL", "==")
                self.position += 2
            
            elif self.origin[self.position] == '=':
                self.actual = Token("ASSIG", "=")
                self.position += 1
                
            elif self.origin[self.position] == ';':
                self.actual = Token('ENDC', ';')
                self.position += 1

            elif self.origin[self.position] == '!':
                self.actual = Token('NOT', '!')
                self.position += 1

            elif self.origin[self.position] == '>':
                self.actual = Token('GREATER', '>')
                self.position += 1

            elif self.origin[self.position] == '<':
                self.actual = Token('LESS', '<')
                self.position += 1

            elif(self.origin[self.position] == "&" and self.origin[self.position + 1] == "&"):
                self.actual = Token("AND", "&&")
                self.position += 2

            elif(self.origin[self.position] == "|" and self.origin[self.position + 1] == "|"):
                self.actual = Token("OR", "||")
                self.position += 2

            else:
                raise NameError("Token inválido.")
        return self.actual