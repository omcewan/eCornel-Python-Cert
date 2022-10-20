"""
Module to demonstrate how to modify a list in a for-loop.

This function does not use the accumulator pattern, because we are not trying
to make a new list.  Instead, we wish to modify the original list.  Note that
you should never modify the list you are looping over (this is bad practice).
So we loop over the range of positions instead.

You may want to run this one in the Python Tutor for full effect.

Author: Walker M. White (wmw2)
Date:   May 24, 2019
"""


def add_one(lst):
    """
    (Procedure) Adds 1 to every element in the list
    
    Example: If a = [1,2,3], add_one(a) changes a to [2,3,4]
    
    Parameter lst: The list to modify
    Precondition: lst is a list of all numbers (either floats or ints)
    """
    size = len(lst)
    for k in range(size):
        lst[k] = lst[k]+1
    # procedure; no return


# Add this if using the Python Tutor
#a = [1,2,3]
#add_one(a)
