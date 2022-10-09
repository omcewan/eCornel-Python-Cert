"""
A function using range to compute a sum of squares

Author: Walker M. White
Date:   April 15, 2019
"""


def sum_squares(n):
    """
    Returns: sum of squares from 1 to n-1
    
    Example: sum_squares(5) is 1+4+9+16 = 30
    
    Parameter n: The number of steps
    Precondition: n is an int > 0
    """
    # Accumulator
    total = 0
    
    for x in range(n):
        total = total + x*x
    
    return total
