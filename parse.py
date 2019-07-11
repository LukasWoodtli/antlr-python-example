#!/usr/bin/env python3
import sys
from antlr4 import *
from parser.CPP14Lexer import CPP14Lexer
from parser.CPP14Parser import CPP14Parser
from parser.CPP14Listener import CPP14Listener



class MyListener(CPP14Listener):
    def __getattribute__(self, name):
        attr = object.__getattribute__(self, name)
        if hasattr(attr, '__call__'):
            def newfunc(*args, **kwargs):
                #print('before calling %s with args %s and %s' % (attr.__name__, str(args), str(kwargs)))
                result = attr(*args, **kwargs)
                #print('done calling %s' % attr.__name__)
                return result

            return newfunc
        else:
            return attr

    def enterPreprocessingDirective(self, context):
        print(context.start.text)



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
