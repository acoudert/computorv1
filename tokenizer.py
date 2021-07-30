INTEGER, XPOWER, PLUS, MINUS, MUL, DIV, EQUAL, EOF = (
    "INTEGER", "XPOWER", "PLUS", "MINUS", "MUL", "DIV", "EQUAL", "EOF"
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
        self.eq = eq
        self.i = 0
        self.char = self.eq[self.i]

    def error(self):
        raise Exception("Invalid equation")
    
    def extract_token(self):
        while self.char:
            if self.char.isdigit():
                return Token(INTEGER, self.__integer())
            elif self.char == "X":
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

    def __integer(self):
        res = ""
        while self.char and self.char.isdigit():
            res += self.char
            self.__advance()
        return int(res)

    def __xpower(self):
        self.__advance()
        if self.char == None:
            return 1
        if self.char == '^':
            self.__advance()
            return self.__integer()
        elif self.char in operators:
            return 1
        self.error()

