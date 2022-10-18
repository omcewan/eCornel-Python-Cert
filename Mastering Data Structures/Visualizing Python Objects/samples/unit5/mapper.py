"""
Module to demonstrate the idea behind map

This module implements the map function.  It also has several support
functions to show how you can leverage it to process data. You may want to run
this one in the Python Tutor for full effect.

Author: Walker M. White (wmw2)
Date:   May 24, 2019
"""


def add_one(x):
    """
    Returns x+1

    Parameter x: The number to add to
    Precondition: x is an int or float
    """
    return x+1


def negate(x):
    """
    Returns -x

    Parameter x: The number to add to
    Precondition: x is an int or float
    """
    return -x


def map(f,data):
    """
    Returns a copy of data, f applied to each entry

    Parameter f: The function to apply
    Precondition: f is a function taking exactly one argument

    Parameter data: The data to process
    Precondition: data a tuple, each entry satisfying precond of f
    """
    accum = ()
    for item in data:
         accum = accum + ( f(item), )
    return accum


# Add this if using the Python Tutor
#a = (1,2,3)
#b = map(add_one, a)
#c = map(negate, a)
