class Assembler:
    @staticmethod
    def initAssembly():
        with open('Assembler/assembly.asm', 'w') as file:
            for line in open('Assembler/startAssembly.txt'):
                file.write(line)

    @staticmethod
    def receiveCommand(command):
        with open("Assembler/assembly.asm", "a") as file:
            file.write("\n" + command)
    
    @staticmethod
    def endAssembly():
        with open("Assembler/assembly.asm", "a") as file:
            for line in open('Assembler/endAssembly.txt'):
                file.write(line)

class Node:
    i = 0
    def __init__(self):
        self.value = None
        self.children = []
        self.id = Node.newID()

    def Evaluate(self, st):
        pass

    @staticmethod
    def newID():
        Node.i += 1
        return Node.i

class BinOp(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children
        self.id = Node.newID()

    def Evaluate(self, st):
        res = 0
        left_child = self.children[0].Evaluate(st)
        Assembler.receiveCommand("PUSH EBX")
        right_child = self.children[1].Evaluate(st)
        Assembler.receiveCommand("POP EAX")
            
        if self.value == '+':
            Assembler.receiveCommand("ADD EAX, EBX")
            Assembler.receiveCommand("MOV EBX, EAX")
            res = left_child[0] + right_child[0]
        elif self.value == '-':
            Assembler.receiveCommand("SUB EAX, EBX")
            Assembler.receiveCommand("MOV EBX, EAX")
            res = left_child[0] - right_child[0]
        elif self.value == '*':
            Assembler.receiveCommand("IMUL EBX")
            Assembler.receiveCommand("MOV EBX, EAX")
            res = left_child[0] * right_child[0]
        elif self.value == '/':
            Assembler.receiveCommand("DIV EBX")
            Assembler.receiveCommand("MOV EBX, EAX")
            res = left_child[0] // right_child[0]
        elif self.value == '>':
            Assembler.receiveCommand("CMP EAX, EBX")
            Assembler.receiveCommand("CALL binop_jg")
            res = left_child[0] > right_child[0]
        elif self.value == '<':
            Assembler.receiveCommand("CMP EAX, EBX")
            Assembler.receiveCommand("CALL binop_jl")
            res = left_child[0] < right_child[0]
        elif self.value == '==':
            Assembler.receiveCommand("CMP EAX, EBX")
            Assembler.receiveCommand("CALL binop_je")
            res = left_child[0] == right_child[0]
        elif self.value == '||':
            Assembler.receiveCommand("OR EAX, EBX")
            Assembler.receiveCommand("MOV EBX, EAX")
            res = bool(left_child[0]) or bool(right_child[0])
        elif self.value == '&&':
            Assembler.receiveCommand("AND EAX, EBX")
            Assembler.receiveCommand("MOV EBX, EAX")
            res = bool(left_child[0]) and bool(right_child[0])
        if(type(res) == bool):
            return (res, "bool")
        return (res, "int")

class UnOp(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children
        self.id = Node.newID()

    def Evaluate(self, st):
        value = self.children[0].Evaluate(st)[0]
        if self.value == '+':
            Assembler.receiveCommand("MOV EBX, " + str(value))
            return (value, "int")
        elif self.value == '-':
            Assembler.receiveCommand("MOV EBX, -" + str(value))
            return (-value, "int")
        elif self.value == '!':
            Assembler.receiveCommand("MOV EBX, !" + str(value))
            return (not value, "bool")


class IntVal(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children
        self.id = Node.newID()

    def Evaluate(self, st):
        Assembler.receiveCommand("MOV EBX, " + str(self.value))
        return (self.value, "int")


class BoolVal(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children
        self.id = Node.newID()

    def Evaluate(self, st):
        if(self.value == "true"):
            Assembler.receiveCommand("MOV EBX, True")
            return (True, "bool")
        elif(self.value == "false"):
            Assembler.receiveCommand("MOV EBX, False")
            return (False, "bool")
        else:
            raise NameError("Erro: variável não booleana. Utilize 'true' ou 'false'.")

class StringVal(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children
        self.id = Node.newID()

    def Evaluate(self, st):
        return (self.value, "string")



class NoOp(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children
        self.id = Node.newID()

    def Evaluate(self, st):
        pass

class AssignmentOp(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children
        self.id = Node.newID()

    def Evaluate(self, st):
        value = self.children[1].Evaluate(st)
        Assembler.receiveCommand("MOV [EBP" + str(st.getter(self.value)[2]) +"], EBX")
        return st.setter(self.children[0], value[0])

        

class DeclaratorOP(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children
        self.id = Node.newID()

    def Evaluate(self, st):
        Assembler.receiveCommand("PUSH DWORD 0")
        return st.declarator(self.children[0], self.children[1])


class PrintOp(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children
        self.id = Node.newID()

    def Evaluate(self, st):
        self.children[0].Evaluate(st)
        Assembler.receiveCommand("PUSH EBX")
        Assembler.receiveCommand("CALL print")
        Assembler.receiveCommand("POP EBX")


class IdentifierOp(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children
        self.id = Node.newID()

    def Evaluate(self, st):
        Assembler.receiveCommand("MOV EBX, [EBP" + str(st.getter(self.value)[2]) + "]")
        return st.getter(self.value)

class BlockOp(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children
        self.id = Node.newID()

    def Evaluate(self, st):
        for node in self.children:
            node.Evaluate(st)

class WhileOp(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children
        self.id = Node.newID()

    def Evaluate(self, st):
        Assembler.receiveCommand("LOOP_" + str(self.id) + ": ")
        self.children[0].Evaluate(st)
        Assembler.receiveCommand("CMP EBX, False")
        Assembler.receiveCommand("JE EXIT_" + str(self.id))
        self.children[1].Evaluate(st)
        Assembler.receiveCommand("JMP LOOP_" + str(self.id))
        Assembler.receiveCommand("EXIT_" + str(self.id) + ": ")
 
class IfOp(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children
        self.id = Node.newID()

    def Evaluate(self, st):
        self.children[0].Evaluate(st)
        Assembler.receiveCommand("CMP EBX, True")
        Assembler.receiveCommand("JE IF_" + str(self.id))
        if len(self.children) == 3:
            self.children[2].Evaluate(st)
        Assembler.receiveCommand("JMP END_IF_" + str(self.id))
        Assembler.receiveCommand("IF_" + str(self.id) + ": ")
        self.children[1].Evaluate(st)
        Assembler.receiveCommand("END_IF_" + str(self.id) + ": ")
            

class InputOp(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children
        self.id = Node.newID()

    def Evaluate(self, st):
        res = int(input())
        return (res,'int')
class SymbolTable:
    def __init__(self):
        self.dic_var = {}
        self.shift = 0

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
            self.dic_var[var] = (val, self.dic_var[var][1], self.dic_var[var][2])

        else:
            raise NameError("Erro: variável não declarada")

    #Funcao para declarar variavel
    def declarator(self, var, tp):
        self.shift -= 4
        self.dic_var[var] = (None, tp, self.shift)

