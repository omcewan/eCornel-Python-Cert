"""
Module to demonstrate how tuple expansion works in a function call.

In a function call, tuple expansion splits the tuple and assigns each entry
to a function parameter in order.  The applications for this are a little
niche (expansion in the function definition is more common), but they are useful
when you want to read function arguments from a file.  You read them into a
single list, and then pass that to a function via expansion.

This can be confusing, so you will want to run this one in the Python Tutor
for full effect.

Author: Walker M. White (wmw2)
Date:   May 24, 2019
"""


def add(x, y):
    """
    Returns x+y
    
    Parameter x: The first number to add
    Precondition: x is an int or float
    
    Parameter y: The second number to add
    Precondition: y is an int or float
    """
    return x+y


# Try this in the Python Tutor
#a = (1,2)
#b = add(*a)
#c = (1,2,3)
#d = add(*c)
