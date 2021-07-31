from sys import exit, stderr

class Options:
    options = {
            "h": ["help", False],
            "v": ["verbose", False], 
            "f": ["fraction", False], 
        }

    def __init__(self, argv):
        if len(argv) < 2:
            self.error()
        self.eq_index = 0
        for i in range(1, len(argv)):
            if self.__isEquationDef(argv[i]):
                if self.eq_index != 0:
                    self.error()
                self.eq_index = i
                continue
            self.__parseArg(argv[i])
        if self.options['h'][1] == True:
            self.displayHelp()
    
    def error(self):
        print("Invalid arguments", file=stderr)
        exit(2)

    def displayHelp(self):
        print("Usage: python3 main.py [OPTION]... EQUATION")
        print("{}Quadratic EQUATION solver.".format(" " * 7))
        print("Options:")
        print("{}-h, --help    : This help".format(" " * 7))
        print("{}-v, --verbose : Produce verbose output".format(" " * 7))
        print("{}-f, --fraction: Display result as fraction".format(" " * 7))
        exit(0)

    # Privates
    def __isEquationDef(self, arg):
        if any([c.isdigit() or c == '+' or c == '=' for c in arg]):
            return True
        return False

    def __parseArg(self, arg):
        if len(arg) < 2 or arg[0] != '-':
            self.error()
        if arg[1] == '-':
            if len(arg) == 2:
                self.error()
            i = 0
            if arg[2] not in self.options.keys():
                self.error()
            if arg[2:] != self.options[arg[2]][0]:
                self.error()
            self.options[arg[2]][1] = True
        else:
            for c in arg[1:]:
                if c not in self.options.keys():
                    self.error()
                self.options[c][1] = True
