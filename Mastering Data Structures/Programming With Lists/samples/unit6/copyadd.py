"""
Module to demonstrate how to use the accumulator pattern on lists

This module has two versions of a function copy_add_one, which creates a copy
of a tuple/list, with 1 added to each element.

Author: Walker M. White (wmw2)
Date:   May 24, 2019
"""


def tup_add_one(tup):
    """
    Returns: a copy of tup with 1 added to every element
    
    Parameter tup: The tuple to copy
    Precondition: tup is a tuple of all numbers (either floats or ints)
    """
    copy = ()  # accumulator
    for x in tup:
        x = x+1
        copy = copy+(x,)      # add to end of copy
    return copy


def list_add_one(lst):
    """
    Returns: a copy of lst with 1 added to every element
    
    Parameter lst: The list to copy
    Precondition: lst is a list of all numbers (either floats or ints)
    """
    copy = []  # accumulator
    for x in lst:
        x = x+1
        copy.append(x)        # add to end of copy
    return copy
