"""
Module with a function to compute the distance between two points.

This version of the function shows tuples are not always the best solution to
this problem.

Author: Walker M. White
Date:   May 24, 2019
"""
import math


def distance(p0,p1):
    """
    Returns the distance between the two points p0 and p1

    Parameter p0: The second point
    Precondition: p0 is a tuple with exactly three elements,
    each of which is a float

    Parameter p1: The second point
    Precondition: p1 is a tuple with exactly three elements,
    each of which is a float.
    """
    assert type(p0) == tuple, repr(p0)+' is not a tuple'
    assert len(p0) == 3, repr(p0)+' has the incorrect length'
    assert type(p0[0]) == float, repr(p0[0])+' is not a float'
    assert type(p0[1]) == float, repr(p0[1])+' is not a float'
    assert type(p0[2]) == float, repr(p0[2])+' is not a float'
    assert type(p1) == tuple, repr(p1)+' is not a tuple'
    assert len(p1) == 3, repr(p1)+' has the incorrect length'
    assert type(p1[0]) == float, repr(p1[0])+' is not a float'
    assert type(p1[1]) == float, repr(p1[1])+' is not a float'
    assert type(p1[2]) == float, repr(p1[2])+' is not a float'

    # Get the square differences between each set of coordinates
    d2x = (p0[0]-p1[0])*(p0[0]-p1[0])
    d2y = (p0[1]-p1[1])*(p0[1]-p1[1])
    d2z = (p0[2]-p1[2])*(p0[2]-p1[2])
    return math.sqrt(d2x+d2y+d2z)
