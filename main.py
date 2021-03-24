import re 
import node as nd
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
        new_code = re.sub("[/][*]\s*(.*?)\s*[*][/]", "", code)
        return new_code

class Token:
    
    """
    TIPOS DE TOKENS:
    - INT   (123)
    - PLUS  ("+")
    - MINUS ("-")
    - MULT  ("*")
    - DIV   ("/")
    - OP    ("(")
    - CP    (")")
    - EOF   (end of file)
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
            else:
                raise NameError("Token inválido.")

        return self.actual

class Parser:
    """
    Função para identificar parênteses e operações unitárias(+ e - como sinais de positivo e negativo) e realiza-la antes das operações básicas (*/+-)
    """
    def parserFactor():
        # resultado = 0
        if Parser.tokenizer.actual.type == 'INT':
            res = nd.IntVal(Parser.tokenizer.actual.value, [])
            # resultado = Parser.tokenizer.actual.value
            Parser.tokenizer.selectNext()
        elif Parser.tokenizer.actual.type == 'OP':
            Parser.tokenizer.selectNext()
            # resultado = Parser.parserExpression()
            res = Parser.parserExpression()
            if Parser.tokenizer.actual.type == 'CP':
                Parser.tokenizer.selectNext()
            else:
                raise NameError("Erro: parênteses não fechado")
        elif Parser.tokenizer.actual.type == 'PLUS':
            Parser.tokenizer.selectNext()
            children = [Parser.parserFactor()]
            res = nd.UnOp('+', children)
            # resultado = resultado + Parser.parserFactor()
        elif Parser.tokenizer.actual.type == 'MINUS':
            Parser.tokenizer.selectNext()
            children = [Parser.parserFactor()]
            res = nd.UnOp('-', children)
            # resultado = resultado - Parser.parserFactor()
        else:
            raise NameError("Token Inválido.")

        # return resultado
        return res
    """
    Função para procurar por operações de MULT e DIV e realiza-las antes das de PLUS e MINUS.
    """
    def parserTerm():
        # resultado = Parser.parserFactor()
        res = Parser.parserFactor()
        while Parser.tokenizer.actual.type == 'MULT' or Parser.tokenizer.actual.type == 'DIV':
            if Parser.tokenizer.actual.type == 'MULT':
                Parser.tokenizer.selectNext()
                children = [res, Parser.parserFactor()]
                res = nd.BinOp('*', children)
                # resultado = resultado * Parser.parserFactor()

            elif Parser.tokenizer.actual.type == 'DIV':
                Parser.tokenizer.selectNext()
                children = [res, Parser.parserFactor()]
                res = nd.BinOp('/', children)
                # resultado = resultado // Parser.parserFactor()

        # return resultado
        return res


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
        # resultado = Parser.parserTerm()
        res = Parser.parserTerm()
        while Parser.tokenizer.actual.type == 'PLUS' or Parser.tokenizer.actual.type == 'MINUS':
            if Parser.tokenizer.actual.type == 'PLUS':
                Parser.tokenizer.selectNext()
                children = [res, Parser.parserTerm()]
                res = nd.BinOp('+', children)
                # resultado = resultado + Parser.parserTerm()

            elif Parser.tokenizer.actual.type == 'MINUS':
                Parser.tokenizer.selectNext()
                children = [res, Parser.parserTerm()]
                res = nd.BinOp('-', children)
                # resultado = resultado - Parser.parserTerm()
        # return resultado
        return res
        
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
    r = Parser.run(string)
    print(r.Evaluate())
