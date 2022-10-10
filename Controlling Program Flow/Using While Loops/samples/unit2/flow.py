"""
A module that shows off flow in a while loop

Author: Walker M. White
Date:   April 15, 2019
"""


def sum_squares2(n):
    """
    Returns: sum of squares from 1 to n-1
    
    Example: sum_squares(5) is 1+4+9+16 = 30
    
    Parameter n: The number of steps
    Precondition: n is an int > 0
    """
    # Accumulator
    total = 0
    
    print('Before while')
    x = 0
    while x < n:
        print('Start loop '+str(x))
        total = total + x*x
        x = x+1
        print('End loop ')
    print('After while')
    
    return total
