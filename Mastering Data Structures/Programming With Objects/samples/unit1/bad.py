"""
Module with a function to compute the distance between two points.

This version of the function shows why it is so unwieldy to rely on the
primitive types (and why we want more complex types)

Author: Walker M. White
Date:   May 24, 2019
"""
import math


def distance(x0,y0,z0,x1,y1,z1):
    """
    Returns the distance between the two points (x0,y0,y1) and (x1,y1,z1)

    Parameter x0: The x-coordinate of the first point
    Precondition: x0 is a float

    Parameter y0: The y-coordinate of the first point
    Precondition: y0 is a float

    Parameter z0: The z-coordinate of the first point
    Precondition: z0 is a float

    Parameter x1: The x-coordinate of the second point
    Precondition: x1 is a float

    Parameter y1: The y-coordinate of the second point
    Precondition: y1 is a float

    Parameter z1: The x-coordinate of the second point
    Precondition: z1 is a float
    """
    assert type(x0) == float, repr(x0)+' is not a float'
    assert type(y0) == float, repr(y0)+' is not a float'
    assert type(z0) == float, repr(z0)+' is not a float'
    assert type(x1) == float, repr(x1)+' is not a float'
    assert type(y1) == float, repr(y1)+' is not a float'
    assert type(z1) == float, repr(z1)+' is not a float'

    # Get the square differences between each set of coordinates
    d2x = (x0-x1)*(x0-x1)
    d2y = (y0-y1)*(y0-y1)
    d2z = (z0-z1)*(z0-z1)
    return math.sqrt(d2x+d2y+d2z)
