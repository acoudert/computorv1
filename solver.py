from interpreter import Interpreter

class Solver:
    
    width = 19

    def __init__(self, eq):
        interpreter = Interpreter(eq)
        self.left, self.right = interpreter.interpret()
        self.reduced = self.__calculateReduced()
        self.degree = self.__calculateDegree()
        self.solution = self.__calculateSolution()
        self.width = 23 if self.solution[0] is "The two solutions are:" else self.width

    def printReduced(self):
        out = []
        for i in range(len(self.left)):
            if self.reduced[i]:
                out.append("{}".format(self.reduced[i]) if i == 0 else "{} * X^{}".format(self.reduced[i], i))
        print("Reduced form:".ljust(self.width), end="")
        if not out:
            print("0", end="")
        for b in out:
            if b[0] == "-":
                print("-", b[1:], end="") if b is out[0] else print(" -", b[1:], end="")
            else:
                print(" +" if b is not out[0] else "+", b, end="")
        print(" = 0")
    
    def printPolynomialDegree(self):
        print("Polynomial degree: ".ljust(self.width), end="")
        print("{}".format(self.degree))

    def printDiscriminant(self):
        if hasattr(self, "discriminant"):
            print("Discriminant:".ljust(self.width), self.discriminant, sep="")

    def printSolution(self):
       print(self.solution[0])
       [print(sol.rjust(self.width+ len(sol))) for sol in self.solution[1]]

    # Privates
    def __calculateReduced(self):
        return [self.left[i] - self.right[i] for i in range(len(self.left))]

    def __calculateDegree(self):
        i = len(self.left) - 1
        while i > 0 and self.reduced[i] == 0:
            i -= 1
        return i
    
    def __calculateSolution(self):
        if self.__allRealsSolution():
            return ("The solutions are:", ["All real numbers - R"])
        if self.__unsolvable():
            return ("There is no solution.", [])
        if all([i == 0 for i in self.reduced[2:]]):
            return self.__solveDegreeOne()
        if self.degree > 2:
            return ("The polynomial degree is strictly greater than 2, I can't solve.", [])
        self.discriminant = self.__calculateDiscriminant()
        if self.discriminant > 0:
            return self.__solvePositive()
        elif self.discriminant == 0:
            return self.__solveZero()
        else:
            return self.__solveNegative()

    def __allRealsSolution(self):
        return all([i == 0 for i in self.reduced])

    def __unsolvable(self):
        if self.reduced[0] and not any([i for i in self.reduced[1:]]):
            return True
        return False

    def __solveDegreeOne(self):
        sol = (-1) * self.reduced[0] / self.reduced[1]
        return ("The solution is:", ["{:+}".format(sol)])

    def __calculateDiscriminant(self):
        return self.reduced[1] ** 2 - 4 * self.reduced[0] * self.reduced[2]
    
    def __solvePositive(self):
        sola = ((-1) * self.reduced[1] + self.discriminant ** (1/2)) / (2 * self.reduced[2])
        solb = ((-1) * self.reduced[1] - self.discriminant ** (1/2)) / (2 * self.reduced[2])
        return ("The two solutions are:", ["{:+}".format(sola), "{:+}".format(solb)])
    
    def __solveZero(self):
        sol = ((-1) * self.reduced[1]) / (2 * self.reduced[2])
        return ("The solution is:", ["{:+}".format(sol)])

    def __solveNegative(self):
        real = ((-1) * self.reduced[1]) / (2 * self.reduced[2])
        imag = ((-1) * self.discriminant) ** (1/2) / (2 * self.reduced[2])
        sola = complex(real, imag)
        solb = complex(real, (-1) * imag)
        return ("The two solutions are:", ["{:+}".format(sola)[1:-1], "{:+}".format(solb)[1:-1]])
    




