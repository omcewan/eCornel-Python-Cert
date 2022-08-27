"""
A module with an unimplemented function

This module shows a function with enforced preconditions. However, the error
messages are not very good.

Author: Walker M. White
Date:   March 1, 2019
"""
import introcs


def last_name_first(n):
    """
    Returns: copy of n but in the form 'last-name, first-name'
    
    We assume that n is just two names (first and last).  Middle names are
    not supported.
    
    Example:
        last_name_first('Walker White') returns 'White, Walker'
    
    Parameter n: the person's name
    Precondition: n is a string with a single space in it.
    """
    # Enforce the precondition
    assert type(n) == str, 'Precondition violation'
    assert introcs.count_str(n,' ') == 1, 'Precondition violation'
    
    # Compute the value
    end_first = introcs.find_str(n,' ')
    first = n[:end_first]
    last  = n[end_first+1:]
    return last+', '+first
