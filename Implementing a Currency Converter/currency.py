"""
Module for currency exchange
  
This module provides several string parsing functions to implement a simple
currency exchange routine using an online currency service. The primary function
in this module is exchange().
  
Author: Orlando McEwan
Date: 09/02/2022
"""

import introcs

APIKEY = 'nBdQBzGVTsB6WwLgqXN9TLAVop0z8r6ELFTp6KcSenwe'


def before_space(s):
    """
    Returns the substring of s up to, but not including, the first space.

    Example: before_space('Hello World') returns 'Hello'

    Parameter s: the string to slice
    Precondition: s is a string with at least one space in it
    """
    assert type(s) == str
    assert " " in s
    
    space_index = introcs.find_str(s," ")
    # print(space_index, s[:space_index], len(s[:space_index]))
    return s[:space_index]


def after_space(s):
    """
    Returns the substring of s after the first space

    Example: after_space('Hello World') returns 'World'

    Parameter s: the string to slice
    Precondition: s is a string with at least one space in it
    """
    assert type(s) == str
    assert " " in s
    
    space_index = introcs.find_str(s, ' ')
    return s[space_index + 1:]