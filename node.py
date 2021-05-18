class Node:
    def __init__(self):
        self.value = None
        self.children = []

    def Evaluate(self, st):
        pass

class BinOp(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children

    def Evaluate(self, st):
        res = 0
        if (self.children[0].Evaluate(st)[1] == "string"):
            if(self.value == "=="):
                return (self.children[0][0] == self.children[1][0], "bool")
            if (self.children[1][1] == "string"):
                if(self.value == "+"):
                    return (self.children[0][0] + self.children[1][0], "string")
                else:
                    raise NameError("Operação inválida com String")
            elif (self.children[1][1] == "int"):
                if(self.value == "*"):
                    res = self.children[0][0]
                    for i in range(0,self.children[1][0]):
                        res += self.children[0][0]
                    return (res, "string")
                else: 
                    raise NameError("Operação inválida com String")
        else:
            if self.value == '+':
                res = self.children[0].Evaluate(st)[0] + self.children[1].Evaluate(st)[0]
            elif self.value == '-':
                res = self.children[0].Evaluate(st)[0] - self.children[1].Evaluate(st)[0]
            elif self.value == '*':
                res = self.children[0].Evaluate(st)[0] * self.children[1].Evaluate(st)[0]
            elif self.value == '/':
                res = self.children[0].Evaluate(st)[0] // self.children[1].Evaluate(st)[0]
            elif self.value == '>':
                res = self.children[0].Evaluate(st)[0] > self.children[1].Evaluate(st)[0]
            elif self.value == '<':
                res = self.children[0].Evaluate(st)[0] < self.children[1].Evaluate(st)[0]
            elif self.value == '==':
                res = self.children[0].Evaluate(st)[0] == self.children[1].Evaluate(st)[0]
            elif self.value == '||':
                res = self.children[0].Evaluate(st)[0] or self.children[1].Evaluate(st)[0]
            elif self.value == '&&':
                res = self.children[0].Evaluate(st)[0] and self.children[1].Evaluate(st)[0]
            if(type(res) == bool):
                return (res, "bool")
            return (res, "int")

class UnOp(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children

    def Evaluate(self, st):
        if self.value == '+':
            return (self.children[0].Evaluate(st), "int")
        elif self.value == '-':
            return (-self.children[0].Evaluate(st), "int")
        elif self.value == '!':
            return (not self.children[0].Evaluate(st), "bool")


class IntVal(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children

    def Evaluate(self, st):
        return (self.value, "int")

class BoolVal(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children

    def Evaluate(self, st):
        if(self.value == "true"):
            return (True, "bool")
        elif(self.value == "false"):
            return (False, "bool")
        else:
            raise NameError("Erro: variável não booleana. Utilize 'true' ou 'false'.")

class StringVal(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children

    def Evaluate(self, st):
        return (self.value, "string")


class NoOp(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children

    def Evaluate(self, st):
        pass

class AssignmentOp(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children

    def Evaluate(self, st):
        if(self.children[0] in st.dic_var):
            return st.setter(self.children[0], self.children[1].Evaluate(st)[0], self.children[1].Evaluate(st)[1])
        return st.declarator(self.children[0], self.children[1])

class PrintOp(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children

    def Evaluate(self, st):
        if(self.children[0].Evaluate(st)[1] == "bool"):
            if(self.children[0].Evaluate(st)[0]):
                print("true")
            else:
                print("false")
        else:
            print(self.children[0].Evaluate(st)[0])

class IdentifierOp(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children

    def Evaluate(self, st):
        if self.value in st.dic_var:
            return st.getter(self.value)

class BlockOp(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children

    def Evaluate(self, st):
        for node in self.children:
            node.Evaluate(st)

class WhileOp(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children

    def Evaluate(self, st):
        while self.children[0].Evaluate(st)[0]:
            self.children[1].Evaluate(st)
 
class IfOp(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children

    def Evaluate(self, st):
        if self.children[0].Evaluate(st)[0]:
            self.children[1].Evaluate(st)
        elif len(self.children) == 3:
            self.children[2].Evaluate(st)

class InputOp(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children

    def Evaluate(self, st):
        return int(input())
class SymbolTable:
    def __init__(self):
        self.dic_var = {}

    def getter(self, var):
        if var in self.dic_var:
            return self.dic_var[var]
        else:
            raise NameError("Erro: variável não existe")

    def setter(self, var, val, tp):
        if var in self.dic_var:
            if self.dic_var[var][1] == tp:
                self.dic_var[var] = (val, tp)
            else: 
                raise NameError("Erro: tipo da variável não condizente")
        else:
            raise NameError("Erro: variável não declarada")

    #Funcao para declarar variavel
    def declarator(self, var, tp):
        # print("Entrei declarator! var: {} e tp: {}".format(var, tp))
        self.dic_var[var] = (None, tp)

