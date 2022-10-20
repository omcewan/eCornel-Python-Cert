"""
Module with non-mutable functions on lists.

All of these functions make use of accumulators that make new lists.

Author: YOUR NAME HERE
Date: THE DATE HERE
"""


def clamp(alist,min,max):
    """
    Returns a copy of alist where every element is between min and max.
    
    Any number in the list less than min is replaced with min.  Any number
    in the tuple greater than max is replaced with max. Any number between
    min and max is left unchanged.
    
    Examples:
        clamp([-1, 1, 3, 5],0,4) returns [0,1,3,4]
        clamp([-1, 1, 3, 5],-2,8) returns [-1,1,3,-5]
        clamp([-1, 1, 3, 5],-2,-1) returns [-1,-1,-1,-1]
        clamp([],0,4) returns []
    
    Parameter alist: the list to copy
    Precondition: alist is a list of numbers (float or int)
    
    Parameter min: the minimum value for the list
    Precondition: min <= max is a number
    
    Parameter max: the maximum value for the list
    Precondition: max >= min is a number
    """
    pass


def removeall(alist,n):
    """
    Returns a copy of alist, removing all instances of n
    
    Examples:
        removeall([1,2,2,3,1],1) returns [2,2,3]
        removeall([1,2,2,3,1],2) returns [1,3,1]
        removeall([1,2,2,3,1],4) returns [1,2,2,3,1]
        removeall([1,1,1],1) returns []
        removeall([],1) returns []
    
    Parameter alist: the list to copy
    Precondition: alist is a list of numbers (float or int)
    
    Parameter n: the number to remove
    Precondition: n is a number
    """
    pass
