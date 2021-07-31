from tokenizer import FLOAT, XPOWER, PLUS, MINUS, MUL, DIV, EQUAL, EOF, Token, Tokenizer

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
    def __init__(self, tokenizer):
        self.tokenizer = tokenizer
        self.token = self.tokenizer.extract_token()
    
    def error(self):
        raise Exception("Invalid equation")

    def parse(self):
        self.root = self.__priority4()
        return self.root
    
    def displayTree(self):
        print("PARSER:")
        self.__printTree(self.root)
        print()

    # Privates
    def __priority1(self):
        token = self.token
        if token.type == FLOAT:
            self.token = self.tokenizer.extract_token()
            return Num(token)
        elif token.type == XPOWER:
            self.token = self.tokenizer.extract_token()
            return XPower(token)
        return None
    
    def __priority2(self):
        node = self.__priority1()
        while self.token.type in (MUL, DIV):
            token = self.token
            self.token = self.tokenizer.extract_token()
            node = BinOp(node, token, self.__priority1())
        return node
    
    def __priority3(self):
        node = self.__priority2()
        while self.token.type in (PLUS, MINUS):
            token = self.token
            self.token = self.tokenizer.extract_token()
            node = BinOp(node, token, self.__priority2())
        return node

    def __priority4(self):
        node = self.__priority3()
        while self.token.type == EQUAL:
            token = self.token
            self.token = self.tokenizer.extract_token()
            node = BinOp(node, token, self.__priority3())
        return node

    def __printTree(self, node, level=0):
        if node != None:
            self.__printTree(node.right, level + 1)
            print(' ' * 8 * level + '->', node.token)
            self.__printTree(node.left, level + 1)

