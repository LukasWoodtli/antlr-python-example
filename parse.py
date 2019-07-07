#!/usr/bin/env python3
import sys
from antlr4 import *
from parser.CPP14Lexer import CPP14Lexer
from parser.CPP14Parser import CPP14Parser
from parser.CPP14Listener import CPP14Listener



class MyListener(CPP14Listener):
    def __getattribute__(self, name):
        def method(*args):
            print("tried to handle unknown method " + name)
            if args:
                print("it had arguments: " + str(args))

        return method

def main(argv):
    input_stream = FileStream(argv[1])
    lexer = CPP14Lexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = CPP14Parser(stream)
    tree = parser.translationunit()

    printer = MyListener()
    walker = ParseTreeWalker()
    walker.walk(printer, tree)


if __name__ == '__main__':
    main(sys.argv)
