"""
Plugin utilites for the pictool.

This module contains all of the commands supported by the application script pictool.py.
To be a valid command, a function must (1) have a first parameter 'image' for the
image buffer, (2) assign default values to parameters after the first, and (3)
return True if it modifies the image and False if not.  You can use these rules to
make your own plugin utilities.

Only three four functions -- mono, flip, transpose, and rotate -- are required for this
project.  All others are optional, though the folder 'solutions' does contain examples
for each of them.

IMPORTANT: It is highly recommended that these functions enforce the preconditions for 
any parameter after images.  Otherwise, command line typos may be hard to debug.

Author: Orlando McEwan
Date: 10/27/2022
"""


# Function useful for debugging
def display(image):
    """
    Returns False after pretty printing the image pixels, one pixel per line.

    All plug-in functions must return True or False.  This function returns False 
    because it displays information about the image, but does not modify it.

    You can use this function to look at the pixels of a file and see whether the 
    pixel values are what you expect them to be.  This is helpful to analyze a file
    after you have processed it.

    Parameter image: The image buffer
    Precondition: image is a 2d table of RGB objects
    """
    height = len(image)
    width = len(image[0])

    # Find the maximum string size for padding
    maxsize = 0
    for row in image:
        for pixel in row:
            text = repr(pixel)
            if len(text) > maxsize:
                maxsize = len(text)

    # Pretty print the pixels
    print()
    for pos1 in range(height):
        row = image[pos1]
        for pos2 in range(width):
            pixel = row[pos2]

            middle = repr(pixel)
            padding = maxsize-len(middle)

            prefix = '      '
            if pos1 == 0 and pos2 == 0:
                prefix = '[  [  '
            elif pos2 == 0:
                prefix = '   [  '

            suffix = ','
            if pos1 == height-1 and pos2 == width-1:
                suffix = (' '*padding)+' ]  ]'
            elif pos2 == width-1:
                suffix = (' '*padding)+' ],'

            print(prefix+middle+suffix)

    # This function does not modify the image
    return


# Example function illustrating image manipulation
def dered(image):
    """
    Returns True after removing all red values from the given image.

    All plug-in functions must return True or False.  This function returns True 
    because it modifies the image. This function sets the red value to 0 for every 
    pixel in the image.

    Parameter image: The image buffer
    Precondition: image is a 2d table of RGB objects
    """
    # Get the image size
    height = len(image)
    width = len(image[0])

    for row in range(height):
        for col in range(width):
            pixel = image[row][col]
            pixel.red = 0

    # This function DOES modify the image
    return True


# IMPLEMENT THESE FOUR FUNCTIONS
def mono(image, sepia=False):
    """
    Returns True after converting the image to monochrome.

    All plug-in functions must return True or False.  This function returns True 
    because it modifies the image. It converts the image to either greyscale or
    sepia tone, depending on the parameter sepia.

    If sepia is False, then this function uses greyscale.  For each pixel, it computes
    the overall brightness, defined as 

        0.3 * red + 0.6 * green + 0.1 * blue.

    It then sets all three color components of the pixel to that value. The alpha value 
    should remain untouched.

    If sepia is True, it makes the same computations as before but sets green to
    0.6 * brightness and blue to 0.4 * brightness.

    Parameter image: The image buffer
    Precondition: image is a 2d table of RGB objects

    Parameter sepia: Whether to use sepia tone instead of greyscale
    Precondition: sepia is a bool
    """
    # We recommend enforcing the precondition for sepia
    # Change this to return True when the function is implemented

    height = len(image)
    width = len(image[0])

    if sepia == True:
        for row in range(height):
            for col in range(width):
                brightness = 0
                pixel = image[row][col]
                brightness += pixel.red * 0.3
                brightness += pixel.green * 0.6
                brightness += pixel.blue * 0.1
                pixel.red = int(brightness)
                pixel.green = int(0.6 * brightness)
                pixel.blue = int(0.4 * brightness)

        return True

    for row in range(height):
        for col in range(width):
            brightness = 0
            pixel = image[row][col]
            brightness += pixel.red * 0.3
            brightness += pixel.green * 0.6
            brightness += pixel.blue * 0.1
            pixel.red = int(brightness)
            pixel.green = int(brightness)
            pixel.blue = int(brightness)

    return True


def flip(image, vertical=False):
    """
    Returns True after reflecting the image horizontally or vertically.

    All plug-in functions must return True or False.  This function returns True 
    because it modifies the image. By default it reflects the image horizonally,
    or vertically if vertical is True.

    Parameter image: The image buffer
    Precondition: image is a 2d table of RGB objects

    Parameter vertical: Whether to reflect the image vertically
    Precondition: vertical is a bool
    """
    # We recommend enforcing the precondition for vertical
    # Change this to return True when the function is implemented

    height = len(image)

    if vertical == True:
        start = 0
        end = height - 1

        while start < end:
            temp = image[start]
            image[start] = image[end]
            image[end] = temp
            start += 1
            end -= 1

        return True

    for row in range(height):
        image[row] = image[row][::-1]

    return True


def transpose(image):
    """
    Returns True after transposing the image

    All plug-in functions must return True or False.  This function returns True 
    because it modifies the image. It transposes the image, swaping colums and rows.

    Transposing is tricky because you cannot just change the pixel values; you have
    to change the size of the image table.  A 10x20 image becomes a 20x10 image.

    The easiest way to transpose is to make a transposed copy with the pixels from
    the original image.  Then remove all the rows in the image and replace it with
    the rows from the transposed copy.

    Parameter image: The image buffer
    Precondition: image is a 2d table of RGB objects
    """
    # Change this to return True when the function is implementedf

    # copy image
    copy_image = []

    # number of rows of image
    height = len(image)

    # number of columns of image
    width = len(image[0])

    # looping through the column is a vertical looping
    for column in range(width):

        # list to build new row
        new_row = []

        # loop through the row and append the new value as we vertically loop through the rows
        for row in range(height):
            new_row.append(image[row][column])

        # append the new row to the copy list
        copy_image.append(new_row)

    #  clear the image and then loop through the range of rows of the copy image and append to image
    image.clear()

    for row in range(len(copy_image)):
        image.append(copy_image[row])

    return True


def rotate(image, right=False):
    """
    Returns True after rotating the image left of right by 90 degrees.

    All plug-in functions must return True or False.  This function returns True 
    because it modifies the image. By default it rotates the image left, or right
    if parameter right is True.

    To rotate left, transpose and then flip vertically.  To rotate right, flip
    vertically first and then transpose.

    Parameter image: The image buffer
    Precondition: image is a 2d table of RGB objects

    Parameter right: Whether to rotate the image right
    Precondition: right is a bool
    """
    # We recommend enforcing the precondition for right
    # Change this to return True when the function is implemented

    if right == True:
        transpose(image)
        flip(image)

        return True

    transpose(image)
    flip(image, True)

    return True


# ADVANCED OPTIONAL FUNCTIONS
def vignette(image):
    """
    Returns True after vignetting (corner darkening) the current image.

    All plug-in functions must return True or False.  This function returns True 
    because it modifies the image. It simulates vignetting, which is a characteristic 
    of antique lenses. This plus sepia tone helps give a photo an antique feel.

    To compute the vignette, you must compute the distance of each pixel from the
    center.  For any two pixels at position (r0,c0) and (r1,c1), the distance between
    the two is

        dist( (r0,c0), (r1,c1)) = sqrt( (r0-r1)*(r0-r1)+(c0-c1)*(c0-c1) )

    The vignette factor for a pixel at row r, col r is

        1 - (d / H)^2

    where d is the distance from the pixel to the center of the image and H (for the
    half diagonal) is the distance from the center of the image to a corner. To 
    vignette an image, multiply each NON-ALPHA color value by its vignette factor.
    The alpha value should be left untouched.

    Parameter image: The image buffer
    Precondition: image is a 2d table of RGB objects
    """
    # Change this to return True when the function is implemented
    return False


def blur(image, radius=5):
    """
    Returns True after bluring the image.

    To blur an image you loop over all pixels.  For each pixel, you average all colors
    (all 4 values including alpha) in a box centered at the pixel with the given radius.
    For example, suppose you are blurring the pixel at position (4,7) with a radius 2
    blur.  Then you will average the pixels at positions (2,5), (2,6), (2,7), (2,8), 
    (2,9), (3,5), (3,6), (3,7), (3,8), (3,9), (4,5), (4,6), (4,7), (4,8), (4,9), (5,5),
    (5,6), (5,7), (5,8), (5,9), (6,5), (6,6), (6,7), (6,8), and (6,9).  You then assign
    that average value to the pixel.

    If the box goes outside of the image bounds, go to the edge of the image.  So if you
    are blurring the pixel at position (0,1) with a radius 2, you average the pixels
    at positions (0,0), (0,1), (0,2), (0,3), (1,0), (1,1), (1,2), (1,3), (2,0), (2,1), 
    (2,2), and (2,3).

    This calculation MUST be done in a COPY.  Otherwise, you are using the blurred 
    value in future pixel computations (e.g. when you try to blur the pixel to the 
    right of it).  All averages must be computed from the original image.  Use the 
    steps from transpose() to modify the image.

    WARNING: This function is very slow (Adobe's programs use much more complicated
    algorithms and are not written in Python).  Blurring 'Walker.png' with a radius 
    of 30 can take up to 10 minutes.

    Parameter image: The image to blur
    Precondition: image is a 2d table of RGB objects

    Parameter radius: The blur radius
    Precondition: radius is an int > 0
    """
    # We recommend enforcing the precondition for radius
    # Change this to return True when the function is implemented
    return False


def pixellate(image, step=10):
    """
    Returns True after pixellating the image.

    All plug-in functions must return True or False.  This function returns True 
    because it modifies the image. It pixellates the image to give it a blocky feel. 

    To pixellate an image, start with the top left corner (e.g. the first row and column).  
    Average the colors (all 4 values including alpha) of the step x step block to the
    right and down from this corner.  For example, if step is 3, you will average the
    colors at positions (0,0), (0,1), (0,2), (1,0), (1,1), (1,2), (2,0), (2,1), and (2,2).
    After computing the averages, assign each color's (and the alpha's) average value
    to ALL the pixels in the block.

    If there are less than step rows or step columns, go to the edge of the image.  So
    on a image with 2 rows and 4 columns, a step 3 pixellate would process the colors
    at positions  (0,0), (0,1), (0,2), (1,0), (1,1), and (1,2).

    When you are done, skip over step columns to get the the next corner pixel, and 
    repeat  this process again.  Because the blocks do not overlap, it is not necessary 
    to create a copy (like blur). You can reassign the pixels before moving to the next 
    block. For example, suppose step is 3. Then the next block is at position (0,3) and 
    includes the pixels at (0,3), (0,4), (0,5), (1,3), (1,4), (1,5), (2,3), (2,4), 
    and (2,5).  

    Continue the process looping over rows and columns to get a pixellated image.

    Parameter image: The image to pixelate
    Precondition: image is a 2d table of RGB objects

    Parameter step: The number of pixels in a pixellated block
    Precondition: step is an int > 0
    """
    # We recommend enforcing the precondition for step
    # Change this to return True when the function is implemented
    return False
