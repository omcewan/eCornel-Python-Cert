"""
A module with an incomplete function.

This function was implemented using the backwards-design technique.

Author: Orlando McEwan
Date: 08/26/2022
"""
import introcs


def second_in_list(s):
    """
    Returns: the second item in comma-separated list

    The final result should not have any whitespace around the edges.

    Example: second_in_list('apple, banana, orange') returns 'banana'
    Example: second_in_list('  do  ,  re  ,  me  ,  fa  ') returns 're'
    Example: second_in_list('z,y,x,w') returns 'y'

    Parameter s: The list of items
    Precondition: s is a string of at least three items separated by commas.
    """
    # assert type(s) == str, "s is not of correct type"
    assert  len(introcs.split(s, ",")) >= 3, "sting doesn't contain at least three items"

    first_comma = introcs.find_str(s, ',')

    second_comma = introcs.find_str(s, ',', first_comma + 1)

    second = introcs.strip(s[first_comma + 1: second_comma])

    return second
