"""
A module with with two tuple functions.

These functions have been fully implemented.

Author: Walker M. White
Date:   April 15, 2019
"""


def sum(tup):
    """
    Returns: the sum of all elements in the tuple
    
    Example: sum((1,2,3)) returns 6
             sum((5,)) returns 5
    
    Parameter tup: the tuple to sum
    Precondition: tup is a nonempty tuple of numbers (either floats or ints)
    """
    result = 0
    
    for x in tup:
        result = result+x
    
    return result


def num_ints(tup):
    """
    Returns: the number of ints in the tuple
    
    Example: num_ints((1,2.0,True)) returns 1
    
    Parameter tup: the tuple to count
    Precondition: tup is a tuple of any mix of types
    """
    result = 0
    
    for x in tup:
        if type(x) == int:
            result = result+1
    
    return result
