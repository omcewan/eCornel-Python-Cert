"""
A module with two functions, one calling the other

Author: Walker M. White (wmw2)
Date:   February 14, 2019
"""


# We can define these in either order
# But both must be defined before any call
def foo(x):
    """
    The first function
    """
    y = x+1
    z = bar(y)
    return z


def bar(x):
    """
    The second function
    """
    y = x-1
    return y


w = foo(2)
