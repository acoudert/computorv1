import re
from sys import exit

INTEGER, XPOWER, PLUS, MINUS, MUL, DIV, EQUAL, EOF = (
    "INTEGER", "XPOWER", "PLUS", "MINUS", "MUL", "DIV", "EQUAL", "EOF"
)
operators = "+-*/="

# Tokenizer
class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __str__(self):
        return "{}: {}".format(self.type, repr(self.value))

class Tokenizer:
    def __init__(self, eq):
        self.eq = eq
        self.i = 0
        self.char = self.eq[self.i]

    def error(self):
        raise Exception("Invalid equation")

    def advance(self):
        self.i += 1
        self.char = self.eq[self.i] if self.i <= len(self.eq) - 1 else None

    def integer(self):
        res = ""
        while self.char and self.char.isdigit():
            res += self.char
            self.advance()
        return int(res)

    def xpower(self):
        self.advance()
        if self.char == None:
            return 1
        if self.char == '^':
            self.advance()
            return self.integer()
        elif self.char in operators:
            return 1
        self.error()

    def extract_token(self):
        while self.char:
            if self.char.isdigit():
                return Token(INTEGER, self.integer())
            elif self.char == "X":
                return Token(XPOWER, self.xpower())
            elif self.char == '+':
                self.advance()
                return Token(PLUS, '+')
            elif self.char == '-':
                self.advance()
                return Token(MINUS, '-')
            elif self.char == '*':
                self.advance()
                return Token(MUL, '*')
            elif self.char == '/':
                self.advance()
                return Token(DIV, '/')
            elif self.char == '=':
                self.advance()
                return Token(EQUAL, '=')
            self.error()
        return Token(EOF, None)

# Nodes
class BinOp:
    def __init__(self, left, token, right):
        self.left = left
        self.token = token
        self.right = right

class Num:
    def __init__(self, token):
        self.left = None
        self.token = token
        self.right = None

class XPower:
    def __init__(self, token, times=1):
        self.left = None
        self.token = token
        self.times = times
        self.right = None

# Parser
class Parser:
    def __init__(self, eq):
        self.tokenizer = Tokenizer(eq)
        self.token = self.tokenizer.extract_token()
    
    def error(self):
        raise Exception("Invalid equation")

    def priority1(self):
        token = self.token
        if token.type == INTEGER:
            self.token = self.tokenizer.extract_token()
            return Num(token)
        elif token.type == XPOWER:
            self.token = self.tokenizer.extract_token()
            return XPower(token)
        return None
    
    def priority2(self):
        node = self.priority1()
        while self.token.type in (MUL, DIV):
            token = self.token
            self.token = self.tokenizer.extract_token()
            node = BinOp(node, token, self.priority1())
        return node
    
    def priority3(self):
        node = self.priority2()
        while self.token.type in (PLUS, MINUS):
            token = self.token
            self.token = self.tokenizer.extract_token()
            node = BinOp(node, token, self.priority2())
        return node

    def priority4(self):
        node = self.priority3()
        while self.token.type == EQUAL:
            token = self.token
            self.token = self.tokenizer.extract_token()
            node = BinOp(node, token, self.priority3())
        return node

    def parse(self):
        self.root = self.priority4()
        self.printTree(self.root)
        print("------")
        return self.root

    def printTree(self, node, level=0):
        if node != None:
            self.printTree(node.left, level + 1)
            print(' ' * 8 * level + '->', node.token)
            self.printTree(node.right, level + 1)

