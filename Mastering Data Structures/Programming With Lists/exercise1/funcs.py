"""
Module demonstrating mutable list functions.

Neither of these functions should use for-lopps.  Instead, they should use 
list methods.

Author: Orlando McEwan
Date: 10/20/2022
"""


def put_in(alist,value):
    """
    Adds a value to a sorted list, resorting as necessary.
    
    Examples:
        If a = [0,2,3,4], put_in(a,1) makes a = [0,1,2,3,4]
        If a = [0,2,3,4], put_in(a,2) makes a = [0,2,2,3,4]
        If a = [], put_in(a,3) makes a = [3]
    
    Parameter a: The list to append to
    Precondition: a is a sorted list of a single type of element
    
    Parameter value: The value to append
    Precondition: value has the same type as the elements of a
    """
    alist.append(value)
    alist.sort()

def rotate(alist):
    """
    Rotates the contents of alist one element to the right.
    
    Rotating a list to the right pushes all elements to the right, and makes
    the previously last element the new first element.
    
    Examples:
        If a = [0,2,3,4], rotate(a) makes a = [4,0,2,3]
        If a = [1], rotate(a) makes a = [1]
    
    Parameter a: The list to rotate
    Precondition: a non-empty list
    """
    # Hint: Read the method description for insert
    last_element = alist.pop()
    alist.insert(0, last_element)
