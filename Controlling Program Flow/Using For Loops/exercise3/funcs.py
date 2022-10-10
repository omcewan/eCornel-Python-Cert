"""
Module with range-based for-loop functions.

Author: Orlando McEwan  
Date: 10/09/2022
"""

def factorial(n):
    """
    Returns n! = n * (n-1) * (n-2) ... * 1
    
    0! is 1.  Factorial is undefined for integers < 0.
    
    Examples:
        factorial(0) returns 1
        factorial(2) returns 2
        factorial(3) returns 6
        factorial(5) returns 120
    
    Parameter n: The integer for the factorial
    Precondition: n is an int >= 0
    """
    
    if n == 0:
        return 1
    
    sum = 1
    
    for num in range(n):
        sum *= n - num

    return sum
        
def revrange(a,b):
    """
    Returns the tuple (b-1, b-2, ..., a)
    
    Note that this tuple is the reverse of tuple(range(a,b))
    
    Parameter a: the "start" of the range
    Precondition: a is an int <= b
    
    Parameter b: the "end" of the range
    Precondition: b is an int >= a
    """
    my_tup = ()
    
    for num in range(b-1, a-1, -1):
        my_tup += (num,)

    return my_tup
