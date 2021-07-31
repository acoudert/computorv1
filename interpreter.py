from tokenizer import FLOAT, XPOWER, PLUS, MINUS, MUL, DIV, EQUAL, EOF, Token
from parser import BinOp, Num, XPower

class Interpreter:
    def __init__(self, parser):
        self.parser = parser
        self.root = self.parser.parse()
    
    def error(self, *args):
        raise Exception("Invalid equation")

    def interpret(self):
        if self.root.token.type != EQUAL:
            self.error()
        self.left = self.__build(self.root.left, "right") # Check if eq is "=..."
        self.right = self.__build(self.root.right, "right")
        self.__updateLeftRightSize()
        return (self.left, self.right)
    
    def displayLeftRight(self):
        print("INTERPRETER:")
        print("left: ", self.left)
        print("right:", self.right)
        print()

    # Privates
    def __updateLeftRightSize(self):
        length = len(self.left) if len(self.left) > len(self.right) else len(self.right)
        [arr.append(0) for arr in (self.left, self.right) for _ in range(len(arr), length)]

    def __build(self, node, desc):
        self.arr = [0]
        n = self.__visit(node, desc)
        if n.token.type == FLOAT: # Get finale value as recursion returns node
            self.arr[0] += n.token.value
        else:
            self.__updateArrSize(n)
            self.arr[n.token.value] += n.times
        return self.arr
    
    def __updateArrSize(self, node):
        [self.arr.append(0) for _ in range(len(self.arr), node.token.value + 1)]

    def __visit(self, node, desc):
        # Return Node
        if node == None and desc == "left": # allow -1= and -1+= handling
            return Num(Token(FLOAT, 0))
        method_name = '_Interpreter__visit_' + type(node).__name__
        visitor = getattr(self, method_name, self.error)
        return visitor(node, desc)

    def __visit_BinOp(self, node, desc):
        # Left and Right updates themselves based on int+int or int+Xpower recursively
        node.left = self.__visit(node.left, "left")
        node.right = self.__visit(node.right, "right")
        if node.token.type == PLUS:
            for n in [node.left, node.right]:
                if n.token.type == XPOWER:
                    self.__updateArrSize(n)
                    self.arr[n.token.value] += n.times
                elif n.token.type == FLOAT:
                    self.arr[0] += n.token.value
            return Num(Token(FLOAT, 0)) 
        elif node.token.type == MINUS:
            for n in [node.left, node.right]:
                if n.token.type == XPOWER:
                    self.__updateArrSize(n)
                    self.arr[n.token.value] += n.times * (-1) if n == node.right else n.times
                elif n.token.type == FLOAT:
                    self.arr[0] += n.token.value * (-1) if n == node.right else n.token.value # first term not to substract
            return Num(Token(FLOAT, 0)) 
        elif node.token.type == MUL:
            if node.left.token.type == FLOAT and node.right.token.type == FLOAT:
                return Num(Token(FLOAT, node.left.token.value * node.right.token.value))
            elif node.left.token.type == XPOWER and node.right.token.type == FLOAT:
                return XPower(Token(XPOWER, node.left.token.value), node.left.times * node.right.token.value)
            elif node.left.token.type == FLOAT and node.right.token.type == XPOWER:
                return XPower(Token(XPOWER, node.right.token.value), node.right.times * node.left.token.value)
        elif node.token.type == DIV:
            if node.left.token.type == FLOAT and node.right.token.type == FLOAT:
                return Num(Token(FLOAT, node.left.token.value / node.right.token.value))
            elif node.left.token.type == XPOWER and node.right.token.type == FLOAT:
                return XPower(Token(XPOWER, node.left.token.value), node.left.times / node.right.token.value)
            elif node.left.token.type == FLOAT and node.right.token.type == XPOWER:
                return XPower(Token(XPOWER, node.right.token.value), node.right.times / node.left.token.value)
        self.error()

    def __visit_Num(self, node, desc):
        return node

    def __visit_XPower(self, node, desc):
        return node
