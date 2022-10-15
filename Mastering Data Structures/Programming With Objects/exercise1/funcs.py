"""
Some functions for working with color.

You do not need to understand how this functions work (yet).

Author: Walker M. White
Data:   August 9, 2019
"""
import introcs


def blend(color1,color2):
    """
    Returns a new color that is the alpha blend of color1 over color2.
    
    This function assumes that the alpha values in the colors are not pre-multiplied.
    
    Parameter color1: The color on top
    Precondition: color1 is an RGB object
    
    Parameter color2: The color underneath
    Precondition: color2 is an RGB object
    """
    gl1 = color1.glColor()
    gl2 = color2.glColor()
    gl3 = [0,0,0,0]
    
    alpha = gl1[3]+gl2[3]*(1-gl1[3])
    
    for pos in range(3):
        gl3[pos] = (gl1[pos]*gl1[3]+gl2[pos]*gl2[3]*(1-gl1[3]))/alpha
        gl3[pos] = round(gl3[pos]*255)
    gl3[3] = round(alpha*255)
    
    return introcs.RGB(*gl3)


def blendUnder(color1,color2):
    """
    Modifies color1 by alpha-blending it underneath color2.
    
    This function assumes that the alpha values in the colors are not pre-multiplied.
    
    Parameter color1: The color to modify
    Precondition: color1 is an RGB object
    
    Parameter color2: The color to blend on top of color1
    Precondition: color2 is an RGB object
    """
    gl1 = color2.glColor()
    gl2 = color1.glColor()
    gl3 = [0,0,0,0]
    
    alpha = gl1[3]+gl2[3]*(1-gl1[3])
    
    for pos in range(3):
        gl3[pos] = (gl1[pos]*gl1[3]+gl2[pos]*gl2[3]*(1-gl1[3]))/alpha
        gl3[pos] = round(gl3[pos]*255)
    gl3[3] = round(alpha*255)
    
    color1.red = gl3[0]
    color1.green = gl3[1]
    color1.blue  = gl3[2]
    color1.alpha = gl3[3]
