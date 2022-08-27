"""
A module to demonstrate how to read error messages.

This module contains multiple bugs.  You will NOT be able to fix them.  We simply want
you to identify them.

This module can be run as a script.  Just uncomment the function calls at the bottom
when directed.

Author: Walker M. White
Date:   July 1, 2019
"""
import introcs


def numerator(s):
    """
    Returns the numerator portion of a fraction (specified as a string)
    
    The value returned is a int.
    
    Example: frac_to_dec('1/2') returns 1
    Example: frac_to_dec('0/5') returns 0
    Example: frac_to_dec('12/1') returns 12
    Example: frac_to_dec('31/64') returns 31
    
    Parameter s: The string representation of the fraction
    Precondition: s is a string of the form 'n/d' where n and d are all digits.
    """
    return int(s[:2])


def denominator(s):
    """
    Returns the numerator portion of a fraction (specified as a string)
    
    The value returned is a int.
    
    Example: frac_to_dec('1/2') returns 2.
    Example: frac_to_dec('0/5') returns 5
    Example: frac_to_dec('5/0') returns 0
    
    Parameter s: The string representation of the fraction
    Precondition: s is a string of the form 'n/d' where n and d are all digits,
    and d is just one digit.
    """
    return int(s[-1])


def frac_to_dec(s):
    """
    Returns the decimal equivalent of a fraction (specified as a string)
    
    The value returned is a float.
    
    Example: frac_to_dec('1/2') returns 0.5
    Example: frac_to_dec('0/5') returns 0.0
    Example: frac_to_dec('12/1') returns 12.0
    Example: frac_to_dec('31/64') returns 0.484375
    
    Parameter s: The string representation of the fraction
    Precondition: s is a string of the form 'n/d' where n and d are all digits.
    """
    n = numerator(s)
    d = denominator(s)
    return n/d


# Uncomment each of these when directed
# x = frac_to_dec("10/0")
# y = frac_to_dec("2/5")
#z = frac_to_dec("ll/25")
#w = frac_to_dec("12/10")

