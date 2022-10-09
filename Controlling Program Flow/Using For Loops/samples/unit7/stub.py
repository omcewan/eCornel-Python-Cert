"""
A module with a function to show off positional for-loops.

This function is a stubs and is not complete

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
    # Create accumulators for first & second parts
    # For each character in s
        # Determine if character is at odd or even pos
        # Add it to the correct accumulator
    # Return tuple with the two parts
