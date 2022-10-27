"""
Module to demonstrate how keyword expansion works in a function definition.

In a function definition, keyword expansion packages all of the arguments
into a single dictions for processing. This allows you to have functions (the
one below) which have many parameters, but most of them are optional.  This is
very popular in GUI libraries where there are a lot of ways to specify a window 
or button.

This can be confusing, so you will want to run this one in the Python Tutor
for full effect.

Author: Walker M. White (wmw2)
Date:   June 7, 2019
"""


def area_of_rectangle(**kw):
    """
    Returns the area of the specified rectangle.
    
    By default, a rectangle is specified as four numbers: (left,bottom,right, top).
    Left and right are the x-coordinates of the left and right edge.  Bottom and top
    are the y-coordinates of the bottoma and top edges.  We assume that normal high
    school coordinates where top is greater than bottom and right is greater than left
    (yes, there are situations this may not be true).
    
    However, this function allows full flexibility for defining a rectangle.  Want to
    specify (left,bottom,width,height) instead?  Or how about (top,right,width,height)?
    We even allow (center,middle,width,height), where convention is that center is the
    x-coordinate of the rectangle center and middle is the y-coordinate of the center.
    
    If the user provides contradictory arguments (e.g. left=1, center=3, and width=10), 
    parameters are prioritized as described below.
    
    Parameter left: The left edge of the rectangle
    Precondition: left is an int or float
    
    Parameter right: The right edge of the rectangle
    Precondition: right is an int or float
    
    Parameter width: The width of the rectangle (ignored if both left & right provided)
    Precondition: width is an int or float
    
    Parameter center: The horizontal center of the rectangle 
    (ignored if any two of left, right, and width provided)
    Precondition: center is an int or float
    
    Parameter bottom: The bottom edge of the rectangle
    Precondition: bottom is an int or float
    
    Parameter top: The top edge of the rectangle
    Precondition: top is an int or float
    
    Parameter height: The height of the rectangle (ignored if both bottom & top provided)
    Precondition: height is an int or float
    
    Parameter middle: The vertical center of the rectangle 
    (ignored if any two of bottom, top, and height provided)
    Precondition: right is an int or float
    """
    # Compute the width of the rectangle
    width = None
    if 'left' in kw and 'right' in kw:
        width = kw['right']-kw['left']
    elif 'width' in kw:
        width = kw['width']
    elif 'center' in kw:
        if 'left' in kw:
            width = 2*(kw['center']-kw['left'])
        elif 'right' in kw:
            width = 2*(kw['right']-kw['center'])
    assert width != None, 'There were not enough arguments to determine the width'
    
    # Compute the height of the rectangle
    height = None
    if 'bottom' in kw and 'top' in kw:
        height = kw['top']-kw['bottom']
    elif 'height' in kw:
        height = kw['height']
    elif 'middle' in kw:
        if 'bottom' in kw:
            height = 2*(kw['center']-kw['bottom'])
        elif 'top' in kw:
            height = 2*(kw['top']-kw['center'])
    assert height != None, 'There were not enough arguments to determine the width'
    
    return width*height


# Try this in the Python Tutor
#a = area_of_rectangle(left=1,bottom=0,right=4,top=5)
#b = area_of_rectangle(center=1,bottom=0,right=4,height=5)
