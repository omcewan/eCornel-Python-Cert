"""
Module to demonstrate a mutable list function

This module demonstrates how you would write a function (procedure) to
modify a list. You may want to run this one in the Python Tutor for full effect.

Author: Walker M. White (wmw2)
Date:   May 24, 2019
"""


def swap(b, h, k):
    """
    Procedure that swaps b[h] and b[k] in b

    Parameter b: The list to modify
    Precondition: b is a mutable list,

    Parameter h: The first position to swap
    Precondition: h is an int and a valid position in the list

    Parameter k: The first position to swap
    Precondition: k is an int and a valid position in the list
    """
    temp= b[h]
    b[h]= b[k]
    b[k]= temp


# Add this if using the Python Tutor
#x = [5,4,7,6,10]
#swap(x,3,4)
