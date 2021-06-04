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
        if (self.children[0].Evaluate(st)[1] == "string" and self.children[1].Evaluate(st)[1] == "string"):
            if(self.value == "=="):
                return (self.children[0].Evaluate(st)[0] == self.children[1].Evaluate(st)[0], "bool")
            elif(self.value == "+"):
                return (self.children[0].Evaluate(st)[0] + self.children[1].Evaluate(st)[0], "string")
            # elif (self.children[1][1] == "int"):
            #     if(self.value == "*"):
            #         res = self.children[0][0]
            #         for i in range(0,self.children[1][0]):
            #             res += self.children[0][0]
            #         return (res, "string")
            
        elif(self.children[0].Evaluate(st)[1] != "string" and self.children[1].Evaluate(st)[1] != "string"):
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
                res = bool(self.children[0].Evaluate(st)[0]) or bool(self.children[1].Evaluate(st)[0])
            elif self.value == '&&':
                res = bool(self.children[0].Evaluate(st)[0]) and bool(self.children[1].Evaluate(st)[0])
            if(type(res) == bool):
                return (res, "bool")
            return (res, "int")
        else: 
                raise NameError("Operação inválida com String")

class UnOp(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children

    def Evaluate(self, st):
        if self.value == '+':
            return (self.children[0].Evaluate(st)[0], "int")
        elif self.value == '-':
            return (-self.children[0].Evaluate(st)[0], "int")
        elif self.value == '!':
            return (not self.children[0].Evaluate(st)[0], "bool")


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
            return st.setter(self.children[0], self.children[1].Evaluate(st)[0])
        else:
            raise NameError("Error: Variável não declarada.")
        

class DeclaratorOP(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children

    def Evaluate(self, st):
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
        if self.children[0].Evaluate(st)[1] == 'string':
            raise NameError("Error: String não é condição.")
        if self.children[0].Evaluate(st)[0]:
            self.children[1].Evaluate(st)
        elif len(self.children) == 3:
            self.children[2].Evaluate(st)

class InputOp(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children

    def Evaluate(self, st):
        res = int(input())
        return (res,'int')
class SymbolTable:
    def __init__(self):
        self.dic_var = {}

    def getter(self, var):
        if var in self.dic_var:
            return self.dic_var[var]
        else:
            raise NameError("Erro: variável não existente")

    def setter(self, var, val): 
        if var in self.dic_var:
            if self.dic_var[var][1] == 'bool':
                val = bool(val)
            if self.dic_var[var][1] == 'int':
                val = int(val)
            if self.dic_var[var][1] == 'string':
                val = str(val)
            self.dic_var[var] = (val, self.dic_var[var][1])

        else:
            raise NameError("Erro: variável não declarada")

    #Funcao para declarar variavel
    def declarator(self, var, tp):
        self.dic_var[var] = (None, tp)

