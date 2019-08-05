#ifndef EXAMPLE_H__
#define EXAMPLE_H__

#include <foo>
#include "bar"


#ifdef CPP_ONLY
using mytype = int;
#endif

class MyClass {
    int foo() { return 3; }
};

#endif