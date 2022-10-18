"""
Module to demonstrate how function variables work

This module demonstrates how you can pass one function as the parameter to
another.  You may want to run this one in the Python Tutor for full effect.

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


def minus_one(x):
    """
    Returns x-1

    Parameter x: The number to add to
    Precondition: x is an int or float
    """
    return x-1


def doit(f,arg):
    """
    Returns the result of the call f(arg)

    Parameter f: the function to call
    Precondition: f a function that takes one argument

    Parameter arg: the function argument
    Precondition: arg satisfies the precondition of f
    """
    return f(arg)


# Add this if using the Python Tutor
a = doit(add_one, 2)
b = doit(minus_one, 2)
