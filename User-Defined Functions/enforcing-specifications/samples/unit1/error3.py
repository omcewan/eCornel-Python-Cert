"""
A module to show off how to interpret an error.

In this example, the error is in the print statement at the bottom.

Author: Walker M. White
Date:   March 1, 2019
"""


def function_1(x,y):
    """
    Returns: result of function_2
    
    Precondition: x is a number
    Precondition: y is a number, y > 0
    """
    return function_2(x,y)


def function_2(x,y):
    """
    Returns: result of function_3
    
    Precondition: x is a number
    Precondition: y is a number, y > 0
    """
    return x/y


# Script Code
print(function_1(1,0))
