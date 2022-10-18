"""
Module to demonstrate the idea behind filter

This module implements the filter function.  It also has several support
functions to show how you can leverage it to process data. You may want to run
this one in the Python Tutor for full effect.

Author: Walker M. White (wmw2)
Date:   May 24, 2019
"""


def iseven(x):
    """
    Returns True if x is even

    Parameter x: The number to add to
    Precondition: x is an int
    """
    return x % 2 == 0


def ispos(x):
    """
    Returns True if x > 0

    Parameter x: The number to add to
    Precondition: x is an int or float
    """
    return x > 0


def filter(f,data):
    """
    Returns a copy of data, removing anything for which f is false

    Parameter f: The function to apply
    Precondition: f is a BOOLEAN function taking exactly one argument

    Parameter data: The data to process
    Precondition: data a tuple, each entry satisfying precond of f
    """
    accum = ()
    for item in data:
        if f(item):
            accum = accum + ( item, )
    return accum


# Add this if using the Python Tutor
#a = (-2,1,4)
#b = filter(iseven, a)
#c = filter(ispos, a)
