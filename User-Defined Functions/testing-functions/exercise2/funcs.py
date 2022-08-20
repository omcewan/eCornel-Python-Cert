"""
Functions for checking a string

This module provides functions for checking a string.

These functions has errors in them and you test them to find the error.

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


def has_y_vowel(s):
    """
    Returns: True if s has y in a "vowel position"
    
    The letter y is a vowel if and only if it is not in the first position.
    So this function checks everything after the first character.
    
    Parameter s: a string to check
    Precondition: s is a non-empty string with all lower case letters
    
    This function may include intentional errors.
    """
    return 'y' in s[1:]
