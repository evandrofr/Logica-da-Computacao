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
        if self.value == '+':
            return self.children[0].Evaluate(st) + self.children[1].Evaluate(st)
        elif self.value == '-':
            return self.children[0].Evaluate(st) - self.children[1].Evaluate(st)
        elif self.value == '*':
            return self.children[0].Evaluate(st) * self.children[1].Evaluate(st)
        elif self.value == '/':
            return self.children[0].Evaluate(st) // self.children[1].Evaluate(st)

class UnOp(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children

    def Evaluate(self, st):
        if self.value == '+':
            return self.children[0].Evaluate(st)
        elif self.value == '-':
            return -self.children[0].Evaluate(st)

class IntVal(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children

    def Evaluate(self, st):
        return self.value

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
        return st.setter(self.children[0], self.children[1].Evaluate(st))

class PrintOp(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children

    def Evaluate(self, st):
        print(self.children[0].Evaluate(st))

class IdentifierOp(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children

    def Evaluate(self, st):
        return st.getter(self.value)

class BlockOp(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children

    def Evaluate(self, st):
        for node in self.children:
            node.Evaluate(st)

class SymbolTable:
    def __init__(self):
        self.dic_var = {}

    def getter(self, var):
        if var in self.dic_var:
            return self.dic_var[var]
        else:
            raise NameError("Erro: variável não existe")

    def setter(self, var, val):
        self.dic_var[var] = val

