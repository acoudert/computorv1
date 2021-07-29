from parser import Token, BinOp, Num, XPower

INTEGER, XPOWER, PLUS, MINUS, MUL, DIV, EQUAL, EOF = (
    "INTEGER", "XPOWER", "PLUS", "MINUS", "MUL", "DIV", "EQUAL", "EOF"
)
operators = "+-*/="

class NodeVisitor:
    def visit(self, node, desc):
        # Return Node
        if node == None and desc == "left": # allow -1= and -1+= handling
            return Num(Token(INTEGER, 0))
        method_name = 'visit_' + type(node).__name__
        visitor = getattr(self, method_name, self.error)
        return visitor(node, desc)

    def error(self, *args):
        raise Exception("Invalid equation")

class Interpreter(NodeVisitor):
    def __init__(self, parser):
        self.parser = parser

    def interpret(self):
        self.root = self.parser.parse()
        if self.root.token.type != EQUAL:
            self.error()
        self.left = self.build(self.root.left, "left")
        self.right = self.build(self.root.right, "right")
        print(self.left, self.right)
        print("------")
        return (self.left, self.right)

    def build(self, node, desc):
        self.arr = [0, 0, 0]
        n = self.visit(node, desc)
        if n.token.type == INTEGER: # Get finale value as recursion returns node
            self.arr[0] += n.token.value
        else:
            self.arr[n.token.value] += n.times
        return self.arr

    def visit_BinOp(self, node, desc):
        # Left and Right updates themselves based on int+int or int+Xpower recursively
        node.left = self.visit(node.left, "left")
        node.right = self.visit(node.right, "right")
        if node.token.type == PLUS:
            for n in [node.left, node.right]:
                if n.token.type == XPOWER:
                    self.arr[n.token.value] += n.times
                elif n.token.type == INTEGER:
                    self.arr[0] += n.token.value
            return Num(Token(INTEGER, 0)) 
        elif node.token.type == MINUS:
            for n in [node.left, node.right]:
                if n.token.type == XPOWER:
                    self.arr[n.token.value] -= n.times
                elif n.token.type == INTEGER:
                    self.arr[0] += n.token.value * (-1) if n == node.right else n.token.value # first term not to substract
            return Num(Token(INTEGER, 0)) 
        elif node.token.type == MUL:
            if node.left.token.type == INTEGER and node.right.token.type == INTEGER:
                return Num(Token(INTEGER, node.left.token.value * node.right.token.value))
            elif node.left.token.type == XPOWER and node.right.token.type == INTEGER:
                return XPower(Token(XPOWER, node.left.token.value), node.left.times * node.right.token.value)
            elif node.left.token.type == INTEGER and node.right.token.type == XPOWER:
                return XPower(Token(XPOWER, node.right.token.value), node.right.times * node.left.token.value)
            else:
                self.error()
        elif node.token.type == DIV:
            if node.left.token.type == INTEGER and node.right.token.type == INTEGER:
                return Num(Token(INTEGER, node.left.token.value / node.right.token.value))
            elif node.left.token.type == XPOWER and node.right.token.type == INTEGER:
                return XPower(Token(XPOWER, node.left.token.value), node.left.times / node.right.token.value)
            elif node.left.token.type == INTEGER and node.right.token.type == XPOWER:
                return XPower(Token(XPOWER, node.right.token.value), node.right.times / node.left.token.value)
            else:
                self.error()

    def visit_Num(self, node, desc):
        return node

    def visit_XPower(self, node, desc):
        if node.token.value < 0 or node.token.value > 2:
            self.error()
        return node
