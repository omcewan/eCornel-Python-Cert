"""
A function to test whether a string is a number.

This module is complete.  It shows how try-except makes it easy.

Author: Walker M. White
Date:   March 30, 2019
"""


def is_number(s):
    """
    Returns True if the string s can be cast to a float.

    Examples:
        is_number('1') is True
        is_number('a') is False
        is_number('1a') is False
        is_number('1.5') is True
        is_number('1.5.4') is False
        is_number('1e-6') is True
        is_number('1-6') is False

    Parameter s: The string to test
    Precondition: s is a string
    """
    try:
        x = float(s)
        return True
    except:
        return False
