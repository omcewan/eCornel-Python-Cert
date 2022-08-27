"""
A module with an unimplemented function

This module shows a function with enforced preconditions.  The stub is_two_words is
not completed.

Author: Walker M. White
Date:   March 1, 2019
"""
import introcs


def is_two_words(w):
    """
    Returns: True if w is 2 words sep by 1 or more spaces.
    
    A word is a string with no spaces. So this means that
        1. The first characters is not a space (or empty)
        2. The last character is not a space (or empty)
        3. There is at least one space in the middle
        4. If there is more than one space, the spaces are adjacent
    
    Parameter w: the string to test
    Precondition: w is a string
    """
    pass


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
    assert is_two_words(n), repr(n)+' has the wrong format'
    
    # Compute the value
    end_first = introcs.find_str(n,' ')
    first = n[:end_first]
    last  = introcs.strip(n[end_first+1:])
    return last+', '+first
