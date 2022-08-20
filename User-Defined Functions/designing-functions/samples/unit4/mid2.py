"""
A module with an unimplemented function

This module has a function is completed.

Author: Walker M. White
Date:   February 14, 2019
"""


def middle(text):
    """
    Returns: middle 3rd of text

    The middle starts at the length divided by 3 (rounded down)
    and continues until 2/3 of the string (rounded down)

    Examples:
        middle('abc')    returns 'b'
        middle('abcd')   returns 'b'
        middle('abcde')  returns 'bc'
        middle('abcdeg') returns 'cd'

    Parameter text: the string to slice
    Precondition: text is a string
    """
    size = len(text)
    start = size//3
    end = 2*size//3
    result = text[start:end]
    return result
