#!/usr/bin/env python3

from sys import argv, exit, stderr
from parser import Parser
from interpreter import Interpreter
from solver import Solver

def main():
    if len(argv) != 2:
        print("Invalid number of arguments", file=stderr)
        exit(1)
    try:
        parser = Parser(argv[1])
        interpreter = Interpreter(parser)
        left, right = interpreter.interpret()
        solver = Solver(left, right)
    except Exception as e:
        print(e)

if __name__ == "__main__":
    main()
