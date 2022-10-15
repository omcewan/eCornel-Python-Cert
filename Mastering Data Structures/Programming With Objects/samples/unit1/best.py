"""
Module with a function to compute the distance between two points.

This version of the function shows why things are so much cleaner with objects.

Author: Walker M. White
Date:   May 24, 2019
"""
import math
from introcs import Point3


def distance(p0,p1):
    """
    Returns the distance between the two points p0 and p1

    Parameter p0: The second point
    Precondition: p0 is a Point3 object

    Parameter p1: The second point
    Precondition: p1 is a Point3 object
    """
    assert type(p0) == Point3, repr(p0)+' is not a Point3 object'
    assert type(p1) == Point3, repr(p1)+' is not a Point3 object'

    # Get the square differences between each set of coordinates
    d2x = (p0.x-p1.x)*(p0.x-p1.x)
    d2y = (p0.y-p1.y)*(p0.y-p1.y)
    d2z = (p0.z-p1.z)*(p0.z-p1.z)
    return math.sqrt(d2x+d2y+d2z)
