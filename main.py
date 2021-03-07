from sys import argv
class Token:
    
    """
    TIPOS DE TOKENS:
    - INT
    - PLUS
    - MINUS
    - EOF (end of file)
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
    """
    Função que realiza o diagrama sintático
    Verificar se o primeiro Token é um número, após isso o próximo token deve ser um sinal.
    Loop de verificação de sinal: caso o sinal seja encontrado devemos identifica-lo, procurar por um número após ele
    e realizar a operação.
    """

    def parserExpression():
        if Parser.tokenizer.actual.type == 'INT':
            # print(Parser.tokenizer.actual.type, Parser.tokenizer.actual.value, "\n")
            resultado = Parser.tokenizer.actual.value
            Parser.tokenizer.selectNext()
            if Parser.tokenizer.actual.type == 'INT':
                raise NameError('Erro sinal não encontrado')
            # print(Parser.tokenizer.actual.type, Parser.tokenizer.actual.value, "\n")
            while Parser.tokenizer.actual.type == 'PLUS' or Parser.tokenizer.actual.type == 'MINUS':
                if Parser.tokenizer.actual.type == 'PLUS':
                    Parser.tokenizer.selectNext()
                    # print(Parser.tokenizer.actual.type, Parser.tokenizer.actual.value, "\n")
                    if Parser.tokenizer.actual.type == 'INT':
                        resultado = resultado + Parser.tokenizer.actual.value
                    else:
                        raise NameError('Erro ao somar')
                elif Parser.tokenizer.actual.type == 'MINUS':
                    Parser.tokenizer.selectNext()
                    # print(Parser.tokenizer.actual.type, Parser.tokenizer.actual.value, "\n")
                    if Parser.tokenizer.actual.type == 'INT':
                        resultado = resultado - Parser.tokenizer.actual.value
                    else:
                        raise NameError('Erro ao subtrair')
                Parser.tokenizer.selectNext()
                # print(Parser.tokenizer.actual.type, Parser.tokenizer.actual.value, "\n")
            if Parser.tokenizer.actual.type == 'INT':
                raise NameError('Erro: sinal não encontrado')
            if Parser.tokenizer.actual.type == 'EOF':
                return resultado
            else:
                raise NameError('Erro: final da operação não encontrado')
        else:
            raise NameError('Erro: expressão não iniciada com um número')
        
    """
    Função que recebe o código que deve ser executado e chama o parserExpression para verifica-lo.
    """
    def run(code):
        Parser.tokenizer = Tokenizer(code)
        return Parser.parserExpression()

if __name__ == "__main__": 
    string = argv[1] # Pegar argumentos da chamada do programa
    print(Parser.run(string))