"""
Module with a function to approximate e ** x.

Author: YOUR NAME HERE
Date: THE DATE HERE
"""


def exp(x,err=1e-6):
    """
    Returns the value of (e ** x) to within the given margin of error.
    
    Do NOT return (math.E ** x).  This function is more precise than that answer.
    
    The value (e ** x) is given by the Power Series
    
        1 + x + (x ** 2)/2 + (x ** 3)/3! + ... + (x ** n)/ n! + ...
    
    We cannot add up infinite values in a program.  So we APPROXIMATE (e ** x)
    by choosing a value n and stopping at that:
    
        1 + x + (x ** 2)/2 + (x ** 3)/3! + ... + (x ** n)/ n!
    
    The error of this approximation is 
    
        abs( (x ** (n+1))/(n+1)!)
    
    which we want less than err.  So to compute e ** x, we just keep computing
    term = (x ** n)/ n! in a loop until this value is less than our error.  If it 
    is not less than the error, we add it to the accumulator, which we return at 
    the end.
    
    Hint: (x**(n+1))/(n+1)!  == (x**n)/n! * x/(n+1)
    Use this fact to simplify your loop.
    
    Parameter x: the exponent for e ** x
    Precondition: x is a numbers
    
    Parameter err: The margin of error (OPTIONAL: default is e-6)
    Precondition: err > 0 is a number
    """
    pass
