"""
Module to demonstrate how tuple expansion works in a function definition.

In a function definition, tuple expansion packages all of the arguments
into a single tuple for processing. This allows you to have functions (like
max), which take a variable number of arguments.

This can be confusing, so you will want to run this one in the Python Tutor
for full effect.

Author: Walker M. White (wmw2)
Date:   May 24, 2019
"""


def max(*tup):
    """
    Returns the maximum value of the arguments passed to this functions
    
    Param tup: The tuple of numbers
    Precond: Each element of tup is an int or float
    """
    themax = None
    for x in tup:
        if themax == None or themax < x:
            themax = x
    return themax


# Try this in the Python Tutor
#a = max(1,2)
#b = max(1,2,3)
