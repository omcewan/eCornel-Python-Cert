"""
A module implementing three different max functions.

These functions show the different ways we can use conditional statements in
defining a function.

Author: Walker M. White
Date:   March 30, 2019
"""


def max1(x,y):
    """
    Returns: max of x, y
    
    Parameter x: first value
    Precondition: x is a number
    
    Parameter y: second value
    Precondition: y is a number
    """
    if x > y:
        return x
    
    return y


def max2(x,y):
    """
    Returns: max of x, y
    
    Parameter x: first value
    Precondition: x is a number
    
    Parameter y: second value
    Precondition: y is a number
    """
    # Put the max inside of y
    if x > y:
        temp = x
        x = y
        y = temp
    return y


def max3(x,y):
    """
    Returns: max of x, y
    
    Parameter x: first value
    Precondition: x is a number
    
    Parameter y: second value
    Precondition: y is a number
    """
    # Put the max inside of temp
    if x > y:
        temp = x
        x = y
        y = temp
    return temp
