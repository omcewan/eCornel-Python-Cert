"""
Module to demonstrate the Point class

This module has a few simple functions that show how to use the Point3 class in
the introcs module.

Author: Walker M. White (wmw2)
Date:   May 24, 2019
"""
from introcs import Point3


def copy2d(p):
    """
    Makes a 2d copy of the point p

    This function makes (and returns) a new point
    that has the same x, y value as p, but whose
    z value is 0.

    Parameter p: The point to copy
    Precondition: p is a Point3 object
    """
    assert type(p) == Point3, repr(p)+' is not a Point3'

    # Make a new point
    q = Point3(p.x,p.y,0)
    return q


def incr_x(q):
    """
    Increments the x coord of p by 1

    Example: (1,2,3) becomes (2,2,3)
    The function does not return a value (it is a procedure).
    It just modifies the point "in place"

    Parameter p: The point to adjust
    Precondition: p is a Point3 object
    """
    assert type(q) == Point3, repr(q)+' is not a Point3'
    q.x = q.x+1
