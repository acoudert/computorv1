FLOAT, XPOWER, PLUS, MINUS, MUL, DIV, EQUAL, EOF = (
    "FLOAT", "XPOWER", "PLUS", "MINUS", "MUL", "DIV", "EQUAL", "EOF"
)
operators = "+-*/="

# Token
class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __str__(self):
        return "{}: {}".format(self.type, repr(self.value))

# Tokenizer
class Tokenizer:
    def __init__(self, eq):
        self.eq = eq.replace(' ', '').upper()
        self.i = 0
        self.char = self.eq[self.i]

    def error(self):
        raise Exception("Invalid equation")
    
    def extract_token(self):
        while self.char:
            if self.char.isdigit():
                return Token(FLOAT, self.__float())
            elif self.char == "X":
                if self.i != 0 and self.eq[self.i-1] not in operators: # 1X^...
                    self.error()
                return Token(XPOWER, self.__xpower())
            elif self.char == '+':
                self.__advance()
                return Token(PLUS, '+')
            elif self.char == '-':
                self.__advance()
                return Token(MINUS, '-')
            elif self.char == '*':
                self.__advance()
                return Token(MUL, '*')
            elif self.char == '/':
                self.__advance()
                return Token(DIV, '/')
            elif self.char == '=':
                self.__advance()
                return Token(EQUAL, '=')
            self.error()
        return Token(EOF, None)

    # Privates
    def __advance(self):
        self.i += 1
        self.char = self.eq[self.i] if self.i <= len(self.eq) - 1 else None

    def __float(self):
        res = ""
        while self.char and self.char.isdigit():
            res += self.char
            self.__advance()
            if self.char == '.':
                if res.count('.') != 0:
                    self.error()
                res += self.char
                self.__advance()
                if not self.char or not self.char.isdigit(): #...1.
                    self.error()
        res = float(res)
        return int(res) if res.is_integer() else res 

    def __xpower(self):
        self.__advance()
        if self.char == None:
            return 1
        if self.char == '^':
            self.__advance()
            if not self.char or not self.char.isdigit(): # X^= || =X^
                self.error()
            res = self.__float()
            if type(res) != int:
                self.error()
            return res
        elif self.char in operators:
            return 1
        self.error()

