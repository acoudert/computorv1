class Solver:
    def __init__(self, left, right):
        self.left = left
        self.right = right
        self.reduced = self.__calculateReduced()
        self.printReduced()
        self.printPolynomialDegree()
        self.solution = self.__calculateSolution()
        print(self.solution)

    def printReduced(self):
        out = []
        for i in range(3):
            if self.reduced[i]:
                out.append("{}".format(self.reduced[i]) if i == 0 else "{} * X^{}".format(self.reduced[i], i))
        print("Reduced form: ", end="")
        if not out:
            print("0", end="")
        for b in out:
            if b[0] == "-":
                print("-", b[1:], end="") if b is out[0] else print(" -", b[1:], end="")
            else:
                print(" +", b, end="")
        print(" = 0")

    def printPolynomialDegree(self):
        print("Polynomial degree: ", end="")
        i = 2
        while i > 0 and self.reduced[i] == 0:
            i -= 1
        print("{}".format(i))

    # Privates
    def __calculateReduced(self):
        return [self.left[i] - self.right[i] for i in range(3)]
    
    def __calculateSolution(self):
        if self.__allRealsSolution():
            return "All reals solve this equation"
        if self.__unsolvable():
            return "This equation cannot be solved"
        if self.reduced[2] == 0:
            return self.__solveDegreeOne()
        self.discriminant = self.__calculateDiscriminant()
        print("Discriminant:", self.discriminant)
        if self.discriminant > 0:
            return self.__solvePositive()
        elif self.discriminant == 0:
            return self.__solveNull()
        else:
            return self.__solveNegative()

    def __allRealsSolution(self):
        return all([i == 0 for i in self.reduced])

    def __unsolvable(self):
        if self.reduced[0] and not self.reduced[1] and not self.reduced[2]:
            return True
        return False

    def __solveDegreeOne(self):
        return "{}".format((-1) * self.reduced[0] / self.reduced[1])

    def __calculateDiscriminant(self):
        return self.reduced[1] ** 2 - 4 * self.reduced[0] * self.reduced[2]
    
    def __solvePositive(self):
        print(self.reduced)
        xa = ((-1) * self.reduced[1] + self.discriminant ** (1/2)) / (2 * self.reduced[2])
        xb = ((-1) * self.reduced[1] - self.discriminant ** (1/2)) / (2 * self.reduced[2])
        return "{} and {}".format(xa, xb)
    
    def __solveNull(self):
        x = ((-1) * self.reduced[1]) / (2 * self.reduced[2])
        return str(x)

    def __solveNegative(self):
        real = ((-1) * self.reduced[1]) / (2 * self.reduced[2])
        imag = ((-1) * self.discriminant) ** (1/2) / (2 * self.reduced[2])
        xa = complex(real, imag)
        xb = complex(real, (-1) * imag)
        return "{} and {}".format(xa, xb)
    




