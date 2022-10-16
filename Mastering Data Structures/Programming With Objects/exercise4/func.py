"""
Module to show off tuple methods.

Neither this module nor the function should import the introcs module.  In addition,
the function should not use a loop or recursion.

Author: Orlando McEwan
Date: 10/16/2022
"""


def replace_first(tup,a,b):
    """
    Returns a copy of tup with the first value of a replaced by b
    
    Examples:
        replace_first((1,2,1),1,3) returns (3,2,1)
        replace_first((1,2,1),4,3) returns (1,2,1)
    
    Parameter tup: The tuple to copy
    Precondition: tup is a tuple of integers
    
    Parameter a: The value to replace
    Precondition: a is an int
    
    Parameter b: The value to replace with
    Precondition: b is an int
    """
    
    if a not in tup:
        new_tup = tup
        return new_tup
    else:
        index_a = tup.index(a)
        new_tup = ()
        if index_a == 0:
            new_tup += (b,)
            new_tup += (tup[index_a + 1:])
            return new_tup
        else:
            new_tup += (tup[:index_a])
            new_tup += (b,)
            new_tup += (tup[index_a + 1:])
            return new_tup
