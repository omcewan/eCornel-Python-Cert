"""
A module with an unimplemented function

This module has a function stub that is partially completed.

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
    end_first = introcs.find_str(n,' ')
    #print(end_first)
    first = n[:end_first]
    #print(first)
    # Get the last name
    # Put them together with a comma
