#!/usr/bin/env python3

from sys import argv, exit
from options import Options
from tokenizer import Tokenizer
from parser import Parser
from interpreter import Interpreter
from solver import Solver

def main():
    try:
        options = Options(argv)
        tokenizer = Tokenizer(argv[options.eq_index])
        parser = Parser(tokenizer)
        interpreter = Interpreter(parser)
        if options.options["v"][1]:
            parser.displayTree()
        solver = Solver(*interpreter.interpret())
        if options.options["v"][1]:
            interpreter.displayLeftRight()
        solver.displayAll(options.options["v"][1], options.options["f"][1])
    except Exception as e:
        print(e)
        exit(1)

if __name__ == "__main__":
    main()
