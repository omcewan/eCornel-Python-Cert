"""
A function for manipulating a string

This module provides a function for manipulating a string.

This function has an error in it and you test it to find the error.

Author: Walker M. White
Date:   February 20, 2019
"""
import introcs


def replace_first(word,a,b):
    """
    Returns: a copy of word with the FIRST instance of a replaced by b
    
    Example: replace_first('crane','a','o') returns 'crone'
    Example: replace_first('poll','l','o') returns 'pool'
    Example: replace_first('crane','cr','b') returns 'bane'
    
    Parameter word: The string to copy and replace
    Precondition: word is a string
    
    Parameter a: The substring to find in word
    Precondition: a is a valid substring of word
    
    Parameter b: The substring to use in place of a
    Precondition: b is a string
    """
    pos = introcs.rfind_str(word,a)
    before = word[:pos]
    after  = word[pos+1:]
    result = before+b+after
    return result
