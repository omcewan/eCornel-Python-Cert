"""
A module to show how global variables work

Author: Walker M. White (wmw2)
Date:   February 14, 2019
"""

a = 4 # Global variable


def get_a():
    """
    Returns value of global variable a
    """
    return a


def mask_a():
    """
    Returns value of local variable a
    """
    a = 3.5
    return a


def change_a():
    """
    Returns altered value of global variable a
    """
    global a
    a = 3.5
    return a
