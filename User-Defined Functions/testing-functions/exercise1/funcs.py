"""
A function for checking a string

This module provides a single function for checking vowles in a string. This 
function has an error in it and you test it to find the error.

Author: Walker M. White
Date:   February 20, 2019
"""


def has_a_vowel(s):
    """
    Returns: True if s has at least one vowel (a, e, i, o, or u)

    This function does not count y as a vowel.

    Parameter s: a string to check
    Precondition: s is a non-empty string with all lower case letters

    This function may include intentional errors.
    """
    return 'a' in s or 'e' in s or 'i' in s or 'o' in s or 'u' in s
