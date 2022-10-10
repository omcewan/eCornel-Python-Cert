"""
Module with more complex for-loop functions.

All of these functions make use of accumulators that make new tuples.

Author: Orlando McEwan
Date: 10/09/2022
"""


def clamp(tup,min,max):
    """
    Returns a copy of tup where every element is between min and max.
    
    Any number in the tuple less than min is replaced with min.  Any number
    in the tuple greater than max is replaced with max. Any number between
    min and max is left unchanged.
    
    Examples:
        clamp((-1, 1, 3, 5),0,4) returns (0,1,3,4)
        clamp((-1, 1, 3, 5),-2,8) returns (-1,1,3,5)
        clamp((-1, 1, 3, 5),-2,-1) returns (-1,-1,-1,-1)
        clamp((),0,4) returns ()
    
    Parameter tup: the tuple to copy
    Precondition: tup is a tuple of numbers (float or int)
    
    Parameter min: the minimum value for the tuple
    Precondition: min <= max is a number
    
    Parameter max: the maximum value for the tuple
    Precondition: max >= min is a number
    """
    
    my_tup = ()
    
    for num in tup:
        if num < min:
            my_tup += (min,)
        elif num > max:
            my_tup += (max,)
        else:
            my_tup += (num,)

    return my_tup

def uniques(tup):
    """
    Returns the number of unique elements in the tuple. 
    
    Examplse: 
        uniques((5, 9, 5, 7)) returns 3
        uniques((5, 5, 1, 'a', 5, 'a')) returns 3
        uniques(()) returns 0
    
    Parameter tup: the tuple to copy
    Precondition: tup is a tuple
    """
    
    if len(tup) == 0:
        return 0
    
    unique = ()
    
    for num in tup:
        if num not in unique:
            unique += (num,)
    
    return len(unique)