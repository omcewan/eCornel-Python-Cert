"""
A module to show while-loops and numerical computations.

This is one of the most powerful uses of a while loop: using it to run
a computation until it converges.  There are a lot of algorithms from
Calculus and Numerical Analysis that work this way.

Author: Walker M. White
Date:   April 15, 2019
"""


def sqrt(c,err=1e-6):
    """
    Returns: the square root of c to with the given margin of error.
    
    We use Newton's Method to find the root of the polynomial f(x) = x^2-c
    
    Newton's Method produces a sequence where
    
        x_(n+1) = x_n - f(x_n)/f'(x_n) = x_n - (x_n*x_n-c)/(2x_n)
    
    which we simplify to
    
        x_(n+1) = x_n/2 + c/2 x_n
    
    We can stop this process and use x_n as an approximation of the square root
    of c.  The error when we do this is less than |x_n*x_n - c|.  So we loop
    until this error is less than err.
    
    Parameter c: The number to compute square root
    Precondition: c >= 0 is a number
    
    Parameter err: The margin of error (OPTIONAL: default is e-6)
    Precondition: err > 0 is a number
    """
    # Start with a rough guess
    x = c/2.0
    
    while abs(x*x-c) > err:
        # Compute next in Newton's Method sequence
        x = x/2.0+c/(2.0*x)
    
    return x
