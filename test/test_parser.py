import unittest
import os
import parse


class TestParser(unittest.TestCase):

    def test_parsing(self):

        expected_model = ["#ifndef EXAMPLE_H__", "#define EXAMPLE_H__",
                          "#include <foo>", '#include "bar"',
                          '#ifdef CPP_ONLY\nusing mytype = int;\n#endif', "#endif"]

        example_cpp_file = os.path.split(__file__)[0]
        example_cpp_file = os.path.join(example_cpp_file, "..", "example.cpp")
        model = parse.parse_file(example_cpp_file)

        model = [chld.source_element_text for chld in model[0].children]

        self.assertSequenceEqual(model, expected_model)


if __name__ == '__main__':
    unittest.main()
