"""
A module with an unimplemented function

This module shows off top-down design with helper functions (not fully complete).

Author: Walker M. White
Date:   February 14, 2019
"""
import introcs


def last_name_first(n):
    """
    Returns: copy of n but in the form 'last-name, first-name'
    
    We assume that n is just two names (first and last).  Middle names are
    not supported.
    
    Examples:
        last_name_first('Walker White') returns 'White, Walker'
        last_name_first('Walker      White') returns 'White, Walker'
    
    Parameter n: the person's name
    Precondition: n is a string in the form 'first-name last-name' with one or
    more spaces between the two names. There are no spaces in either <first-name>
    or <last-name>
    """
    # Find the first name
    first = first_name(n)
    # Find the last name
    last = last_name(n)
    # Put together with comma
    return last+", "+first # Stub


def first_name(n):
    """
    Returns: first name in n
    
    Parameter n: the person's name
    Precondition: n is a string in the form 'first-name last-name' with one or
    more spaces between the two names. There are no spaces in either <first-name>
    or <last-name>
    """
    end = introcs.find_str(n,' ')
    return n[:end]


def last_name(n):
    """
    Returns: first name in n
    
    Parameter n: the person's name
    Precondition: n is a string in the form 'first-name last-name' with one or
    more spaces between the two names. There are no spaces in either <first-name>
    or <last-name>
    """
    return ""
