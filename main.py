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
    def parserOrExpression():
        res = Parser.parserAndExpression()
        while Parser.tokenizer.actual.type == 'OR':
            Parser.tokenizer.selectNext()
            children = [res, Parser.parserAndExpression()]
            res = nd.BinOp('||', children)
        return res

    def parserAndExpression():
        res = Parser.parserEqExpression()
        while Parser.tokenizer.actual.type == 'AND':
            Parser.tokenizer.selectNext()
            children = [res, Parser.parserEqExpression()]
            res = nd.BinOp('&&', children)
        return res

    def parserEqExpression():
        res = Parser.parserRelExpression()
        while Parser.tokenizer.actual.type == 'EQUAL':
            Parser.tokenizer.selectNext()
            children = [res, Parser.parserRelExpression()]
            res = nd.BinOp('==', children)
        return res

    def parserRelExpression():
        res = Parser.parserExpression()
        while Parser.tokenizer.actual.type == 'GREATER' or Parser.tokenizer.actual.type == 'LESS':
            if Parser.tokenizer.actual.type == 'GREATER':
                Parser.tokenizer.selectNext()
                children = [res, Parser.parserExpression()]
                res = nd.BinOp('>', children)

            elif Parser.tokenizer.actual.type == 'LESS':
                Parser.tokenizer.selectNext()
                children = [res, Parser.parserExpression()]
                res = nd.BinOp('<', children)
        return res
    """
    Função para identificar parênteses e operações unitárias(+ e - como sinais de positivo e negativo) e realiza-la antes das operações básicas (*/+-)
    """
    def parserFactor():
        if Parser.tokenizer.actual.type == 'INT':
            res = nd.IntVal(Parser.tokenizer.actual.value, [])
            Parser.tokenizer.selectNext()

        elif Parser.tokenizer.actual.type == tk.TRUE or Parser.tokenizer.actual.type == tk.FALSE:
            res = nd.BoolVal(Parser.tokenizer.actual.value, [])
            Parser.tokenizer.selectNext()

        elif Parser.tokenizer.actual.type == 'STR':
            res = nd.StringVal(Parser.tokenizer.actual.value, [])
            Parser.tokenizer.selectNext()

        elif Parser.tokenizer.actual.type == 'OP':
            Parser.tokenizer.selectNext()
            res = Parser.parserOrExpression()
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
        elif Parser.tokenizer.actual.type == 'NOT':
            Parser.tokenizer.selectNext()
            children = [Parser.parserFactor()]
            res = nd.UnOp('!', children)


        elif Parser.tokenizer.actual.type == 'IDENTIFIER':
            res = nd.IdentifierOp(Parser.tokenizer.actual.value, [])
            Parser.tokenizer.selectNext()
        
        elif Parser.tokenizer.actual.type == tk.READLN:
            Parser.tokenizer.selectNext()
            if Parser.tokenizer.actual.type == 'OP':
                Parser.tokenizer.selectNext()
                if Parser.tokenizer.actual.type == 'CP':
                    Parser.tokenizer.selectNext()
                else:
                    raise NameError("Erro: parênteses não fechado")
            else: 
                raise NameError("Erro: readln é uma função abra e feche parenteses para chama-la")
            res = nd.InputOp("readln", [])
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
        if Parser.tokenizer.actual.type == 'OK':
            Parser.tokenizer.selectNext()
            while Parser.tokenizer.actual.type != 'CK':
                if Parser.tokenizer.actual.type == 'EOF':
                    raise NameError("Erro: bloco não fechado")
                lista_resultado.append(Parser.parserCommand())
            if Parser.tokenizer.actual.type == 'CK':
                    Parser.tokenizer.selectNext()
            else:
                raise NameError("Erro: bloco não fechado")
        else:
            raise NameError("Erro: bloco não aberto")

        return nd.BlockOp("BLOCK", lista_resultado)
        
    """
    Função utilizada para identificar comandando como atribuição de variaveis e print
    Utiliza ; para identificar o fim de um comando
    """

    def parserCommand():
        if Parser.tokenizer.actual.type == 'IDENTIFIER':
            var = Parser.tokenizer.actual.value
            Parser.tokenizer.selectNext()
            if Parser.tokenizer.actual.type == 'ASSIG':
                Parser.tokenizer.selectNext()
                valor = Parser.parserOrExpression()
                res = nd.AssignmentOp(var, [var, valor])
                if Parser.tokenizer.actual.type != "ENDC":
                    raise NameError("Erro: falta ; na atribuição de variavel")
                else:
                    Parser.tokenizer.selectNext()    
            else:
                raise NameError("Erro: sem sinal de recebe (=)")

        elif Parser.tokenizer.actual.type == tk.INT or Parser.tokenizer.actual.type == tk.BOOL or Parser.tokenizer.actual.type == tk.STRING:
            tp = Parser.tokenizer.actual.type
            Parser.tokenizer.selectNext()
            var = Parser.tokenizer.actual.value
            res = nd.DeclaratorOP(var, [var, tp])
            Parser.tokenizer.selectNext()
            if Parser.tokenizer.actual.type != "ENDC":
                raise NameError("Erro: falta ; na declaração")
            else:
                Parser.tokenizer.selectNext()


        elif Parser.tokenizer.actual.type == tk.PRINTLN:
            Parser.tokenizer.selectNext()
            if Parser.tokenizer.actual.type == 'OP':
                Parser.tokenizer.selectNext()
                val = Parser.parserOrExpression()
                if Parser.tokenizer.actual.type == 'CP':
                    Parser.tokenizer.selectNext()
                    if Parser.tokenizer.actual.type != "ENDC":
                        raise NameError("Erro: falta ; no println")
                    else:
                        Parser.tokenizer.selectNext()
                else:
                    raise NameError("Erro: parênteses não fechado")
            res = nd.PrintOp("println", [val])

        elif Parser.tokenizer.actual.type == tk.WHILE:
            Parser.tokenizer.selectNext()
            if Parser.tokenizer.actual.type == 'OP':
                Parser.tokenizer.selectNext()
                val = Parser.parserOrExpression()
                if Parser.tokenizer.actual.type == 'CP':
                    Parser.tokenizer.selectNext()
                    res = nd.WhileOp('while', [val,Parser.parserCommand()])
                else:
                    raise NameError("Erro: parênteses não fechado")
            else:
                raise NameError("Erro: parênteses não aberto")

        elif Parser.tokenizer.actual.type == "OK":
            res = Parser.parserBlock()

            

        elif Parser.tokenizer.actual.type == tk.IF:
            children = []
            Parser.tokenizer.selectNext()
            if Parser.tokenizer.actual.type == 'OP':
                Parser.tokenizer.selectNext()
                children.append(Parser.parserOrExpression())
                if Parser.tokenizer.actual.type == 'CP':
                    Parser.tokenizer.selectNext()
                    children.append(Parser.parserCommand())
                else:
                    raise NameError("Erro: parênteses não fechado")
                if Parser.tokenizer.actual.type == tk.ELSE:
                    Parser.tokenizer.selectNext()
                    children.append(Parser.parserCommand())
            else:
                raise NameError("Erro: parênteses não aberto")
            res = nd.IfOp('if', children)

        elif Parser.tokenizer.actual.type == "ENDC":
            res = nd.NoOp(0, [])
            Parser.tokenizer.selectNext()

        else:
            res = nd.NoOp(0, [])
            raise NameError("Erro: Comando inválido")

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
    
    nd.Assembler.initAssembly()
    r = Parser.run(entrada)
    r.Evaluate(st)
    nd.Assembler.endAssembly()
