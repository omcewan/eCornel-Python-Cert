"""
An empty module to illustrate function stubs.

This module will contain function stubs, which are callable but do not do anything.

Author: Orlando McEwan
Date: 08/20/2022
"""
import introcs


def initials(n):
    """
    Returns: The initials <first>. <last>. of the given name.

    We assume that n is just two names (first and last). Middle names are
    not supported.

    Example: initials('John Smith') returns 'J. S.'
    Example: initials('Walker White') returns 'W. W.'

    Parameter n: the person's name
    Precondition: n is in the form 'first-name last-name' with one space 
    between names. There are no spaces in either <first-name> or <last-name>
    """
    first = n[0]
    
    pos = introcs.find_str(n, ' ') + 1
    
    last = n[pos]
    
    # result = + first + '. ' + last + '.'
    result = f'{first}. {last}.'
    
    # Return the initials for n
    return result
