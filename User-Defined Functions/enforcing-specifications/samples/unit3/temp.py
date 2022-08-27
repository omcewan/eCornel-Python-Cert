"""
Conversion functions between fahrentheit and centrigrade

This module shows off two functions for converting temperature back and forth
between fahrenheit and centigrade.  It also shows how to use variables to
represent "constants", or values that we give a name in order to remember them
better.

Author: Walker M. White (wmw2)
Date:   March 1, 2019
"""

# Functions
def to_centigrade(x):
    """
    Returns: x converted to centigrade
    
    The value returned has type float.
    
    Parameter x: the temperature in fahrenheit
    Precondition: x is a float
    """
    assert type(x) == float, repr(x)+' is not a float'
    return 5*(x-32)/9.0


def to_fahrenheit(x):
    """
    Returns: x converted to fahrenheit
    
    The value returned has type float.
    
    Parameter x: the temperature in centigrade
    Precondition: x is a float
    """
    assert type(x) == float, repr(x)+' is not a float'
    return 9*x/5.0+32


# Constants
FREEZING_C = 0.0   # Temperature water freezes in centrigrade

FREEZING_F = to_fahrenheit(FREEZING_C)

BOILING_C = 100.0  # Temperature water freezes in centrigrade

BOILING_F = to_fahrenheit(BOILING_C)
