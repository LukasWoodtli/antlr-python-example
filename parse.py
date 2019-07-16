#!/usr/bin/env python3
import sys
from antlr4 import *
from antlr4.BufferedTokenStream import *
from parser.CPP14Lexer import CPP14Lexer
from parser.CPP14Parser import CPP14Parser
from parser.CPP14Listener import CPP14Listener


class CppElement:
    def __init__(self, source_element_text):
        self.source_element_text = source_element_text
        self.children = []

    def __repr__(self):
        return self.source_element_text

    def get_source_text(self):
        return self.source_element_text

    def append_child(self, element):
        self.children.append(element)

    def get_children(self):
        return self.children


class CppFile(CppElement):

    def __init__(self):
        super().__init__("")


class PreprocessingDirective(CppElement):
    pass


class MyListener(CPP14Listener):
    def __init__(self):
        self.cpp_file_model = []  # stack of parsed elements

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

    def get_model(self):
        return self.cpp_file_model

    def _enter_element_add_to_stack(self, element):
        self.cpp_file_model.append(element)

    def _exit_element_remove_from_stack(self):
        if len(self.cpp_file_model) > 1:
            last_element = self.cpp_file_model.pop()
            self.cpp_file_model[len(self.cpp_file_model) - 1].append_child(last_element)

    def enterTranslationunit(self, context):
        cpp_file = CppFile()
        self._enter_element_add_to_stack(cpp_file)

    def exitTranslationunit(self, context):
        self._exit_element_remove_from_stack()


    def enterPreprocessingDirective(self, context):
        directive = PreprocessingDirective(context.getText())
        self._enter_element_add_to_stack(directive)

    def exitPreprocessingDirective(self, context):
        self._exit_element_remove_from_stack()


def parse_file(file):
    input_stream = FileStream(file)
    lexer = CPP14Lexer(input_stream)
    stream = BufferedTokenStream(lexer)
    parser = CPP14Parser(stream)
    tree = parser.translationunit()

    listener = MyListener()
    walker = ParseTreeWalker()
    walker.walk(listener, tree)

    return listener.get_model()


if __name__ == '__main__':
    for element in parse_file(sys.argv[1]):
        print(element)
