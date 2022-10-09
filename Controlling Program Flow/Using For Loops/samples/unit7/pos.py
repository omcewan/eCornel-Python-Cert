"""
A module with a function to show off positional for-loops.

This function has been fully implemented, and is correct.

Author: Walker M. White
Date:   April 15, 2019
"""
import introcs


def partition(s):
    """Returns: a tuple splitting s in two parts
    
    The 1st element of the tuple is consists of all characters in even
    positions (starting at 0), while the 2nd element is the odd positions.
    
    Examples:
        partition('abcde') is ('ace','bd')
        partition('aabb') is ('ab', 'ab’)
    
    Parameter s: the string to partition
    Precondition: s is a string
    """
    first = ''
    second = ''
    
    for pos in range(len(s)):
        if pos % 2 == 0:
            first = first + s[pos]
        else:
            second = second + s[pos]
    
    return (first,second)
