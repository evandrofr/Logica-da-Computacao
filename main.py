import re   
from sys import argv

class PreProc:
    """
    Função criada para eliminar comentários no estilo /* comentário */
    Foi utilizado RegEx para procurar os padrões.
    Primeiro procura-se os sinais de '/*' nessa ordem, então procura-se 0 ou mais espaços em branco seguidos de
    zero ou mais caracteres que não sejam o fechamento de comentário '*/', então procura-se por mais espaços em brancos
    para então procurar pela sequencia '*/'.
    """
    def filter_comment(code):
        new_code = re.sub("[/][*]\s*(.*)\s*[*][/]", "", code)
        return new_code
class Token:
    
    """
    TIPOS DE TOKENS:
    - INT
    - PLUS
    - MINUS
    - MULT
    - DIV
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
            if self.origin[self.position] == '*':
                self.actual = Token('MULT', '*')
                self.position += 1
            if self.origin[self.position] == '/':
                self.actual = Token('DIV', '/')
                self.position += 1
        return self.actual

class Parser:
    """
    Função para procurar por operações de MULT e DIV e realiza-las antes das de PLUS e MINUS.
    """


    def parserTerm():
        if Parser.tokenizer.actual.type == 'INT':
            resultado = Parser.tokenizer.actual.value
            Parser.tokenizer.selectNext()
            while Parser.tokenizer.actual.type == 'MULT' or Parser.tokenizer.actual.type == 'DIV':
                if Parser.tokenizer.actual.type == 'MULT':
                    Parser.tokenizer.selectNext()
                    if Parser.tokenizer.actual.type == 'INT':
                        resultado = resultado * Parser.tokenizer.actual.value
                    else:
                        raise ValueError("Erro ao multiplicar")
                elif Parser.tokenizer.actual.type == 'DIV':
                    Parser.tokenizer.selectNext()
                    if Parser.tokenizer.actual.type == 'INT':
                        resultado = resultado / Parser.tokenizer.actual.value
                    else:
                        raise ValueError("Erro ao dividir")
                Parser.tokenizer.selectNext()
        else:
            raise NameError('Erro: expressão não iniciada com um número')

        return resultado


    """
    Função que realiza o diagrama sintático
    Verificar se o primeiro Token é um número, após isso o próximo token deve ser um sinal.
    Loop de verificação de sinal: caso o sinal seja encontrado devemos identifica-lo, procurar por um número após ele
    e realizar a operação.
    Nessa versão foi implementada a função parserTerm que procura pelos sinais de multiplicação e divisão antes dos de
    soma e subtração. Sempre que encontramos os sinais + ou - chamamos o parserTerm para procurar enventuais sinais * ou /
    que devem ser efetuado antes.
    """

    def parserExpression():
        resultado = Parser.parserTerm()
        while Parser.tokenizer.actual.type == 'PLUS' or Parser.tokenizer.actual.type == 'MINUS' or Parser.tokenizer.actual.type == 'MULT' or Parser.tokenizer.actual.type == 'DIV':
            if Parser.tokenizer.actual.type == 'PLUS':
                Parser.tokenizer.selectNext()
                if Parser.tokenizer.actual.type == 'INT':
                    resultado = resultado + Parser.parserTerm()
                else:
                    raise NameError('Erro ao somar')
            elif Parser.tokenizer.actual.type == 'MINUS':
                Parser.tokenizer.selectNext()
                if Parser.tokenizer.actual.type == 'INT':
                    resultado = resultado - Parser.parserTerm()
                else:
                    raise NameError('Erro ao subtrair')
        return resultado
        
    """
    Função que recebe o código que deve ser executado e chama o parserExpression para verifica-lo.
    """
    def run(code):
        new_code = PreProc.filter_comment(code)
        Parser.tokenizer = Tokenizer(new_code)
        resultado = Parser.parserExpression()
        if Parser.tokenizer.actual.type == "EOF":
            return resultado
        else:
            raise NameError('Erro: final da operação não encontrado')




if __name__ == "__main__": 
    string = argv[1] # Pegar argumentos da chamada do programa
    print(Parser.run(string))