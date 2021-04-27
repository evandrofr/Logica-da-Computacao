import re 
import node as nd
import tokenizer as tk
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

class Parser:
    """
    Função para identificar parênteses e operações unitárias(+ e - como sinais de positivo e negativo) e realiza-la antes das operações básicas (*/+-)
    """
    def parserFactor():
        if Parser.tokenizer.actual.type == 'INT':
            res = nd.IntVal(Parser.tokenizer.actual.value, [])
            Parser.tokenizer.selectNext()
        elif Parser.tokenizer.actual.type == 'OP':
            Parser.tokenizer.selectNext()
            res = Parser.parserExpression()
            if Parser.tokenizer.actual.type == 'CP':
                Parser.tokenizer.selectNext()
            else:
                raise NameError("Erro: parênteses não fechado")
        elif Parser.tokenizer.actual.type == 'PLUS':
            Parser.tokenizer.selectNext()
            children = [Parser.parserFactor()]
            res = nd.UnOp('+', children)
        elif Parser.tokenizer.actual.type == 'MINUS':
            Parser.tokenizer.selectNext()
            children = [Parser.parserFactor()]
            res = nd.UnOp('-', children)

        elif Parser.tokenizer.actual.type == 'IDENTIFIER':
            res = nd.IdentifierOp(Parser.tokenizer.actual.value, [])
            Parser.tokenizer.selectNext()
        else:
            raise NameError("Token Inválido.")

        return res
    """
    Função para procurar por operações de MULT e DIV e realiza-las antes das de PLUS e MINUS.
    """
    def parserTerm():
        res = Parser.parserFactor()
        while Parser.tokenizer.actual.type == 'MULT' or Parser.tokenizer.actual.type == 'DIV':
            if Parser.tokenizer.actual.type == 'MULT':
                Parser.tokenizer.selectNext()
                children = [res, Parser.parserFactor()]
                res = nd.BinOp('*', children)

            elif Parser.tokenizer.actual.type == 'DIV':
                Parser.tokenizer.selectNext()
                children = [res, Parser.parserFactor()]
                res = nd.BinOp('/', children)

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
        res = Parser.parserTerm()
        while Parser.tokenizer.actual.type == 'PLUS' or Parser.tokenizer.actual.type == 'MINUS':
            if Parser.tokenizer.actual.type == 'PLUS':
                Parser.tokenizer.selectNext()
                children = [res, Parser.parserTerm()]
                res = nd.BinOp('+', children)

            elif Parser.tokenizer.actual.type == 'MINUS':
                Parser.tokenizer.selectNext()
                children = [res, Parser.parserTerm()]
                res = nd.BinOp('-', children)
        return res
    """
    Função utilizada para identificar blocos de comandos que se iniciam com a palavra reservada BEGIN
    e terminando com a palavra reservada END.
    """

    def parserBlock():
        lista_resultado=[]
        if Parser.tokenizer.actual.type == 'BEGIN':
            Parser.tokenizer.selectNext()
            if Parser.tokenizer.actual.type == 'ENTER':
                Parser.tokenizer.selectNext()
                while Parser.tokenizer.actual.type != 'END':
                    lista_resultado.append(Parser.parserCommand())
                    if Parser.tokenizer.actual.type != 'ENTER':
                        raise NameError("Erro: não quebrou a linha do Command")
                    else:
                        Parser.tokenizer.selectNext()

                return nd.BlockOp("COMMAND", lista_resultado)

            else:
                raise NameError("Erro: não quebrou a linha do begin")
        else:
            raise NameError("Erro: não abriu BEGIN")
        
    """
    Função utilizada para identificar comandando como atribuição de variaveis e print
    Utiliza \n para identificar o fim de um comando
    """

    def parserCommand():
        if Parser.tokenizer.actual.type == 'IDENTIFIER':
            var = Parser.tokenizer.actual.value
            Parser.tokenizer.selectNext()
            if Parser.tokenizer.actual.type == 'ASSIG':
                sinal = Parser.tokenizer.actual.value 
                Parser.tokenizer.selectNext()
                res = nd.AssignmentOp(sinal, [var, Parser.parserExpression()])    
            else:
                raise NameError("Erro: sem sinal de recebe (=)")
        elif Parser.tokenizer.actual.type == 'PRINT':
            Parser.tokenizer.selectNext()
            res = nd.PrintOp("PRINT", [Parser.parserExpression()])
        elif Parser.tokenizer.actual.type == 'BEGIN':
            res = Parser.parserBlock()
            Parser.tokenizer.selectNext()

        else:
            res = NoOp(0, [])

        return res
        
    """
    Função que recebe o código que deve ser executado e chama o parserExpression para verifica-lo.
    """
    def run(code):
        new_code = PreProc.filter_comment(code)
        Parser.tokenizer = tk.Tokenizer(new_code)
        resultado = Parser.parserBlock()
        Parser.tokenizer.selectNext()
        while Parser.tokenizer.actual.type == 'ENTER':
            Parser.tokenizer.selectNext()
        if Parser.tokenizer.actual.type == "EOF":
            return resultado
        else:
            raise NameError('Erro: final da operação não encontrado')




if __name__ == "__main__":
    if (len(argv) == 2):
        string = argv[1] # Pegar argumentos da chamada do programa
    else:
        raise NameError('Erro: o programa recebe um único arquivo .c como argumento')
    st = nd.SymbolTable()
    with open (string, 'r') as file:
        entrada = file.read()
    r = Parser.run(entrada)
    r.Evaluate(st)
