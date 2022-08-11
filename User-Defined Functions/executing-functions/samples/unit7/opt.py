"""
A module to show off optional arguments

Author: Walker M. White (wmw2)
Date:   February 14, 2019
"""


def point_str(x,y=0,z=0):
    """
    Returns a string repr of a point.
    
    Example: point_str(1,2,3) returns '(1.0,2.0,3.0)'

    Parameter x: the x coordinate
    Precondition: x is a number

    Parameter y: the y coordinate
    Precondition: y is a number

    Parameter z: the x coordinate
    Precondition: z is a number
    """
    # Convert all numbers to floats
    x = float(x)
    y = float(y)
    z = float(z)
    result = '('+str(x)+','+ str(y)+','+ str(z)+')'
    return result
