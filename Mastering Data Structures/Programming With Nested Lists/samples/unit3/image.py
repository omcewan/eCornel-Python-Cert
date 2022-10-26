"""
Module to demonstrate what an image might look like in memory.

This module has a function that constructs a table of RGB objects, which is what an
image is in memory.  The image is the smilely face represented in smile.xlsx.

Author: Walker M. White
Date:   June 7, 2019
"""
import introcs


def wh():
    """
    Returns an RGB object representing a white pixel.
    
    This function is created to make smile() more legible.
    """
    return introcs.RGB(255,255,255)


def bk():
    """
    Returns an RGB object representing a black pixel.
    
    This function is created to make smile() more legible.
    """
    return introcs.RGB(0,0,0)


def yw():
    """
    Returns an RGB object representing a yellow pixel.
    
    This function is created to make smile() more legible.
    """
    return introcs.RGB(255,250,0)


def smile():
    """
    Returns a table of RGB objects representing a smilely face image.
    """
    row0 = [wh(), wh(), wh(), wh(), wh(), wh(), wh(), wh(), wh()]
    row1 = [wh(), wh(), wh(), yw(), yw(), yw(), wh(), wh(), wh()]
    row2 = [wh(), wh(), yw(), yw(), yw(), yw(), yw(), wh(), wh()]
    row3 = [wh(), yw(), yw(), bk(), yw(), bk(), yw(), yw(), wh()]
    row4 = [wh(), yw(), yw(), yw(), yw(), yw(), yw(), yw(), wh()]
    row5 = [wh(), yw(), bk(), yw(), yw(), yw(), bk(), yw(), wh()]
    row6 = [wh(), wh(), yw(), bk(), bk(), bk(), yw(), wh(), wh()]
    row7 = [wh(), wh(), wh(), yw(), yw(), yw(), wh(), wh(), wh()]
    row8 = [wh(), wh(), wh(), wh(), wh(), wh(), wh(), wh(), wh()]
    
    return [row0,row1,row2,row3,row4,row5,row6,row7,row8]

