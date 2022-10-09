"""
A function to turn a (string) fraction into a float.

This function shows the challenges of testing a function with try-except.

Author: Walker M. White
Date:   March 30, 2019
"""
import introcs


def eval_frac(s):
    """
    Returns string s, which represents a fraction, as a float
    
    If s does not represent a fraction, it returns None.
    
    Parameter s: The string to evaluate
    Precondition: s is a string with a / in it
    """
    assert type(s) == str, repr(s)+' is not a string'
    assert '/' in s, repr(s)+' is missing a /'
    
    try:
        pos = introcs.find_str(s,'/')
        top = int(s[:pos])              # Error?
        bot = int(s[pos+1:])            # Error?
        return top/bot                  # Error?
    except:
        return None
