"""
A module with an unimplemented function

This module shows a function with enforced preconditions.

Author: Walker M. White
Date:   March 1, 2019
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
    Precondition: n is in the form 'first-name last-name' with one or more
    spaces between the two names. There are no spaces in either <first-name>
    or <last-name>
    """
    # Enforce the precondition
    assert type(n) == str, repr(n)+' is not a string'
    assert ' ' in n, repr(n)+' is missing a space'
    
    # Compute the value
    end_first = introcs.find_str(n,' ')
    first = n[:end_first]
    last  = introcs.strip(n[end_first+1:])
    return last+', '+first
