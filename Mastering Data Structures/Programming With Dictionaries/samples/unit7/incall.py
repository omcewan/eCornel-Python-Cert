"""
Module to demonstrate how keyword expansion works in a function call.

In a function call, keyword expansion assigns each value to a variable whose name
matches the key.  The keys must be strings of variable names for this to work.
This useful when you have functions with A LOT of parameters (such as 10 or more).

This can be confusing, so you will want to run this one in the Python Tutor
for full effect.

Author: Walker M. White (wmw2)
Date:   June 7, 2019
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
#d = {'x':1,'y':2}
#a = add(**d)
#e = {'x':1,'y':2,'z':3}
#b = add(**e)
