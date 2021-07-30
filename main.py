#!/usr/bin/env python3

from sys import argv, exit, stderr
from options import Options
from solver import Solver

def main():
    if len(argv) != 2:
        print("Invalid number of arguments", file=stderr)
        exit(1)
    try:
        options = Options(argv)
        solver = Solver(argv[1])
        solver.printReduced()
        solver.printPolynomialDegree()
        solver.printDiscriminant()
        solver.printSolution()
    except Exception as e:
        print(e)

if __name__ == "__main__":
    main()
