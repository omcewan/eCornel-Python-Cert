"""
A module to demonstrate the difference between print and return

The command print displays a value on screen, but it does not use that value
when it evaluates the function.  The command return instructs a function call
to evaluate to that value.

Author: Walker M. White
Date:   February 14, 2019
"""

def print_plus(n):
    """
    Prints the value of n+1 to the screen.
    """
    print(n+1)


def return_plus(n):
    """
    Returns: the value of n+1 to the screen.
    """
    return (n+1)
