"""
Module with mutable functions on lists.

All of these functions modify their list arguments.

Author: Orlando McEwan
Date: 10/20/2022
"""


def clamp(alist, min, max):
    """
    Modifies alist so that every element is between min and max.

    Any number in the list less than min is replaced with min.  Any number
    in the tuple greater than max is replaced with max. Any number between
    min and max is left unchanged.

    Examples:
        If a = [-1, 1, 3, 5], clamp(a,0,4) changes a to [0,1,3,4]
        If a = [-1, 1, 3, 5], clamp(a,-2,8) changes a to [-1,1,3,-5]
        If a = [-1, 1, 3, 5], clamp(a,-2,-1) changes a to [-1,-1,-1,-1]
        If a = [], clamp(a,0,4) returns []

    Parameter alist: the list to modify
    Precondition: alist is a list of numbers (float or int)

    Parameter min: the minimum value for the list
    Precondition: min <= max is a number

    Parameter max: the maximum value for the list
    Precondition: max >= min is a number
    """
    for num in range(len(alist)):
        if alist[num] < min:
            alist[num] = min
        elif alist[num] > max:
            alist[num] = max


def removeall(alist, n):
    """
    Removes all instances of n from alist

    Examples:
        If a = [1,2,2,3,1], removeall(a,1) changes a to [2,2,3]
        If a = [1,2,2,3,1], removeall(a,2) changes a to [1,3,1]
        If a = [1,2,2,3,1], removeall(a,4) changes a to [1,2,2,3,1]
        If a = [1,1,1], removeall(a,1) changes a to []
        If a = [], removeall(a,1) changes a to []

    Parameter alist: the list to modify
    Precondition: alist is a list of numbers (float or int)

    Parameter n: the number to remove
    Precondition: n is a number
    """
    count = 0
    for index in range(len(alist)):
        if alist[index - count] == n:
            alist.remove(n)
            count += 1
