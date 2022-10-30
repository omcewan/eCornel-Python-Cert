"""
The verification functions for Course 4 scripts

This file is insecurely available to students, but if they find it and modify it, they
really did not need this course.

Author: Walker M. White
Date:   July 31, 2018
"""
from PIL import Image as CoreImage
import os, os.path, sys
import importlib, importlib.util
import traceback
import inspect
import builtins
import copy
import ast

from modlib import load_from_path

# For support
import introcs

#mark Constants

# The status codes
TEST_SUCCESS      = 0
FAIL_NO_FILE      = 1
FAIL_BAD_STYLE    = 2
FAIL_CRASHES      = 4
FAIL_INCORRECT    = 5


WORKSPACE = [os.path.expanduser('~'),'workspace']
LOCALSPACE = os.path.split(__file__)[0]
#WORKSPACE = ['..']


#mark -
#mark Helpers

# Localized error codes
DOCSTRING_MISSING   = 1
DOCSTRING_UNCLOSED  = 2
DOCSTRING_NOT_FIRST = 3

def read_file(name):
    """
    Returns the contents of the file or None if missing.
    
    Parameter name: The file name
    Precondition: name is a string
    """
    path = os.path.join(*WORKSPACE,name)
    try:
        with open(path) as file:
            result = file.read()
        return result
    except:
        return None


def get_docstring(text,first=True):
    """
    Returns the docstring as a list of lines
    
    This function returns an error code if there is no initial docstring.
    
    Parameter text: The text to search for a docstring.
    Precondition: text is a string
    
    Parameter text: Whether to require the docstring to be first.
    Precondition: text is a string
    """
    lines = text.split('\n')
    lines = list(map(lambda x: x.strip(),lines))
    
    start = -1
    for pos in range(len(lines)):
        if len(lines[pos]) >= 3 and lines[pos][:3] in ['"""',"'''"]:
            start = pos
            break
    
    if start == -1:
        return DOCSTRING_MISSING
    
    end = -1
    for pos in range(start+1,len(lines)):
        if lines[pos][-3:] == lines[start][:3]:
            end = pos
            break
    
    if end == -1:
        return DOCSTRING_UNCLOSED
    
    if first:
        for pos in range(start):
            if len(lines[pos]) > 0:
                return DOCSTRING_NOT_FIRST
    
    # One last trim
    if len(lines[start]) > 3:
        lines[start] = lines[start][3:]
    else:
        start += 1
    if len(lines[end]) > 3:
        lines[end] = lines[end][:-3]
    else:
        end -= 1
    return lines[start:end+1]


# Localized error codes
NAME_MISSING     = 1
NAME_INCOMPLETE  = 2

def check_name(text):
    """
    Returns TEST_SUCCESS if the name is correct, and error code otherwise
    
    Parameter text: The docstring text as a list.
    Precondition: text is a list of strings
    """
    if not text[-2].lower().startswith('author:'):
        return NAME_MISSING
    if not text[-2][7:].strip():
        return NAME_INCOMPLETE
    if 'your name here' in text[-2][7:].lower():
        return NAME_INCOMPLETE
    return TEST_SUCCESS


# Localized error codes
DATE_MISSING     = 1
DATE_INCOMPLETE  = 2

def check_date(text):
    """
    Returns TEST_SUCCESS if the date is correct, and error code otherwise
    
    Parameter text: The docstring text as a list.
    Precondition: text is a list of strings
    """
    if not text[-1].lower().startswith('date:'):
        return DATE_MISSING
    
    date = text[-1][5:].strip()
    try:
        import dateutil.parser as util
        temp = util.parse(date)
        return TEST_SUCCESS
    except:
        return DATE_INCOMPLETE


pass
#mark -
#mark Image Comparison
def image_opts(options):
    """
    Returns the image options as a string.
    
    Parameter options: the image options
    Precondition: options is a dictionary
    """
    result = '(no options)'
    if  len(options) > 0:
        flag = list(options.items())[0]
        result = '(--'+str(flag[0])+'='+str(flag[1])+')'
    return result


def image_suffix(func,options):
    """
    Returns the suffix for this image operations and options
    
    Parameter func: the image operation
    Precondition: func is a string
     
    Parameter options: the image options
    Precondition: options is a dictionary
    """
    suffix = func
    if len(options) > 0:
        suffix += '-'+'-'.join(options.keys())
    return '-'+suffix


def read_image(file):
    """
    Returns an in-memory image buffer for the given file.
    
    An image buffer is a 2d table of RGB objects.  This is different than the way
    images are represented by the PIL module (which is designed for speed), but it
    is easier for beginners.
    
    This function prints out a simple progress bar to indicate how far along it
    is in loading.  The progress bar consists of several periods followed by 'done'.
    
    If the file does not exist, or there is an error in reading the file, then
    this function returns None.
    
    Paramater file: The image file to read
    Precondition: file is a string
    """
    try:
        path = os.path.join(LOCALSPACE,file)
        image = CoreImage.open(path)
        
        # Extract data from PIL
        image = image.convert("RGBA")
        width  = image.size[0]
        height = image.size[1]
        
        # This is an iterator.  It allows us to "sync" two sequences in the loop
        source = iter(image.getdata())
        
        # Convert PIL data to student-friendly format
        buffer = []
        for r in range(height):
            row = []
            for c in range(width):
                # Get next PIL pixel and convert to RGB object
                tups = next(source)
                row.append(introcs.RGB(*tups))
                
            buffer.append(row)
        
        return buffer
    except:
        traceback.print_exc()
        return None


def verify_image(buffer):
    """
    Returns True if buffer is the correct format for an image buffeer; False otherwise.
    
    The function is used to verify that the code in the plugins module has not 
    corrupted an image before saving it.
    
    Parameter buffer: the candidate image buffer
    """
    if type(buffer) != list or len(buffer) == 0:
        return False
    
    first = buffer[0]
    if type(first) != list or len(first) == 0:
        return false
    
    width = len(first)
    for row in buffer:
        if len(row) != width:
            return False
        for item in row:
            if type(item) != introcs.RGB:
                return False
    
    return True


# Localized error codes
IMAGE_CORRUPT = -1
IMAGE_ROTATE  = -2
IMAGE_SQUASH  = -2

def compare_image(name,func,options):
    """
    Returns comparison information about the function performance on the given image.
    
    This function takes the image with the given name and filters it with the given
    function and options.  It then compares it to the solution image.  If the image
    is corrupted, or has the wrong dimensions, this function returns an error code.
    Otherwise, it returns the percentage difference between the computed result and
    the solution (so a value of 0 is a correct function)
    
    Parameter name: the name of the image (without the .png suffix) to compare
    Precondtion: name is one of 'debug', 'blocks', 'rocket', or 'Japan'
    
    Param func: The filter function
    Precondition: func is a reference to the function in plugins
    
    Parameter options: the image options
    Precondition: options is a dictionary
    """
    suffix = image_suffix(func.__name__,options)
    src = read_image(name+'.png')
    dst = read_image(name+suffix+'.png')
    
    try:
        func(src,**options)
    except:
        return traceback.format_exc(0)
        
    if not verify_image(src):
        return IMAGE_CORRUPT
    elif len(src) != len(dst):
        if len(src[0]) == len(dst):
            return IMAGE_ROTATE
        else:
            return IMAGE_SQUASH
    elif len(src[0]) != len(dst[0]):
        return IMAGE_SQUASH
    
    height = len(src)
    width  = len(src[0])
    total = 0
    for r in range(height):
        for c in range(width):
            if src[r][c] == dst[r][c]:
                total += 1
    
    # Horrible hack to fix the mono problem
    backup = func.__name__ == 'mono' and options != {}
    if backup and total != height*width:
        suffix = image_suffix(func.__name__,{'alt':True})
        dst = read_image(name+suffix+'.png')
    
        nheight = len(src)
        nwidth  = len(src[0])
        ntotal = 0
        for r in range(nheight):
            for c in range(nwidth):
                if src[r][c] == dst[r][c]:
                    ntotal += 1        
        
        total = max(total,ntotal)
    # End of horrible hack
    
    return 1-total/(height*width)


pass
#mark -
#mark Subgraders
def grade_docstring(file,step=0,outp=sys.stdout):
    """
    Returns the test result and score for the docstring.
    
    The step parameter is the phase in the grading pass.  Step 0 is a verification step
    and will stop at the first error found.  Otherwise it will continue through and try 
    to find all errors.
    
    Parameter name: The file name
    Precondition: name is a string of a file in the given workspace
    
    Parameter step: The current verfication/grading step
    Precondition: grade is 0 or 1
    
    Parameter outp: The output stream
    Precondition: outp is a stream writer
    """
    code = read_file(file)
    if code is None:
        outp.write('Could not find the file %s.\n' % repr(file))
        return (FAIL_NO_FILE, 0)
    
    score = 1
    docs = get_docstring(code)
    if type(docs) == int:
        if docs == DOCSTRING_MISSING:
            outp.write('There is no module docstring in %s.\n' % repr(file))
            return (FAIL_BAD_STYLE,0)
        if docs == DOCSTRING_UNCLOSED:
            outp.write('The module docstring is not properly closed.\n')
            return (FAIL_CRASHES,0.1)
        if docs == DOCSTRING_NOT_FIRST:
            outp.write('The module docstring is not the first non-blank line.\n')
            score -= 0.3
        if not step:
            return (FAIL_BAD_STYLE,max(0,score))
    docs = get_docstring(code,False)
    
    test = check_name(docs)
    if test:
        if test == NAME_MISSING:
            outp.write("The second-to-last line in the docstring for %s does not start with 'Author:'\n" % repr(file))
            score -= 0.5
        if test == NAME_INCOMPLETE:
            outp.write("There is no name after 'Author:' in the docstring for %s.\n"  % repr(file))
            score -= 0.4
        if not step:
            return (FAIL_BAD_STYLE,max(0,score))
    test = check_date(docs)
    if test:
        if test == DATE_MISSING:
            outp.write("The last line in the docstring for %s does not start with 'Date:'\n"  % repr(file))
            score -= 0.5
        if test == DATE_INCOMPLETE:
            outp.write("The date after 'Date:' in the docstring for %s is invalid .\n"  % repr(file))
            score -= 0.4
        if not step:
            return (FAIL_BAD_STYLE, max(0,score))
    
    return (TEST_SUCCESS, max(0,score))


def grade_func(file,func,options,step=0,outp=sys.stdout):
    """
    Returns the test result and score for the implementation of func with the given options
    
    The step parameter is the phase in the grading pass.  Step 0 is a verification step
    and will stop at the first error found.  Otherwise it will continue through and try 
    to find all errors.
    
    Parameter file: The file name
    Precondition: file is a string of a file in the given workspace
    
    Parameter step: The current verfication/grading step
    Precondition: grade is 0 or 1
    
    Parameter outp: The output stream
    Precondition: outp is a stream writer
    """
    score = 1
    try:
        plugins = load_from_path(os.path.join(*WORKSPACE,os.path.splitext(file)[0]))
    except AssertionError as e:
        outp.write('Could not find the file %s.\n' % repr(file))
        return (FAIL_NO_FILE, 0)
    except:
        outp.write("The module %s crashed:\n" % repr(file))
        outp.write(traceback.format_exc(0)+'\n')
        return (FAIL_CRASHES, 0)
    
    if not hasattr(plugins,func):
        outp.write("File %s is missing the header for %s.\n" % (repr(file),repr(func)))
        return (FAIL_INCORRECT, 0)
    
    failed = False
    images = ['blocks','debug','rocket','Japan']
    filter = getattr(plugins,func)
    
    for img in images:
        result = compare_image(img,filter,options)
        if type(result) == str:
            outp.write("Function %s %s crashed on image '%s.png'.\n" % (repr(func),image_opts(options),img))
            outp.write(result+'\n\n')
            return (FAIL_INCORRECT, 0)
        elif result == IMAGE_CORRUPT:
            outp.write("Function %s %s has corrupted the image buffer for '%s.png'.\n" % (repr(func),image_opts(options),img))
            return (FAIL_INCORRECT, 0)
        elif result == IMAGE_ROTATE:
            outp.write("Function %s %s mixes up width and height on '%s.png'.\n" % (repr(func),image_opts(options),img))
            score -= 1/len(images)
            failed = True
            return (FAIL_INCORRECT, 0)
            if not step:
                break
        elif result == IMAGE_SQUASH:
            outp.write("Function %s %s produces the wrong dimensions for '%s.png'.\n" % (repr(func),image_opts(options),img))
            score -= 1/len(images)
            failed = True
            return (FAIL_INCORRECT, 0)
            if not step:
                break
        elif result:
            outp.write("Function %s %s was %0.f%% incorrect on '%s.png'.\n" % (repr(func),image_opts(options),100*(result),img))
            score -= 1/len(images)
            failed = True
            return (FAIL_INCORRECT, 0)
            if not step:
                break
    
    # Now try to add more comments using the blocks
    if failed:
        if func == 'mono':
            comment_mono(filter,options,outp)
        elif func == 'flip':
            comment_flip(filter,options,outp)
        elif func == 'transpose':
            comment_transpose(filter,options,outp)
        elif func == 'rotate':
            comment_rotate(filter,options,outp)
        
        if step:
            (FAIL_INCORRECT,max(0,score))
    
    return (TEST_SUCCESS,max(0,score))


def comment_mono(func,options,outp):
    """
    Report specific feedback about a mono operation
    
    Param func: The filter function
    Precondition: func is a reference to the function 'mono'
    
    Parameter options: the image options
    Precondition: options is a dictionary
    
    Parameter outp: The output stream
    Precondition: outp is a stream writer
    """
    suffix = image_suffix('mono',options)
    src = read_image('blocks.png')
    dst = read_image('blocks'+suffix+'.png')
    
    # This would have crashed already
    func(src,**options)
    srcpix1 = src[1][len(src[0])-2]
    dstpix1 = dst[1][len(dst[0])-2]
    srcpix2 = src[len(src)-2][1]
    dstpix2 = dst[len(dst)-2][1]
    corner = src[len(src)-1][0]
    
    if srcpix1.alpha != dstpix1.alpha or srcpix2.alpha != dstpix2.alpha:
        outp.write("The function modified the alpha value (it should not).\n")
    elif corner.alpha != 0:
        outp.write("The function modified the alpha value (it should not).\n")
    elif srcpix1.red != dstpix1.red or srcpix2.red != dstpix2.red:
        outp.write("The brightness calculuation appears to be incorrect.\n")
    elif len(options) == 0:
        if (srcpix1.red != srcpix1.blue or srcpix1.red != srcpix1.green or
            srcpix2.red != srcpix2.blue or srcpix2.red != srcpix2.green):
            outp.write("The function does not set red, green, and blue to the same value.\n")
    elif (srcpix1.green != dstpix1.green or srcpix2.green != dstpix2.green):
        outp.write("The function does not compute the green value correctly.\n")
    elif (srcpix1.blue != dstpix1.blue or srcpix2.blue != dstpix2.blue):
        outp.write("The function does not compute the blue value correctly.\n")
    else:
        outp.write("Compare the incorrect images with the provided solutions.\n")


def comment_flip(func,options,outp):
    """
    Report specific feedback about a flip operation
    
    Param func: The filter function
    Precondition: func is a reference to the function 'flip'
    
    Parameter options: the image options
    Precondition: options is a dictionary
    
    Parameter outp: The output stream
    Precondition: outp is a stream writer
    """
    orig = read_image('blocks.png')
    tran = read_image('blocks.png')
    height = len(orig)
    width  = len(orig[0])
    
    vert = 'vertical' in options and options['vertical']
    # This would have crashed already
    func(tran,**options)
    trantl = tran[0][0]
    trantr = tran[0][width-1]
    tranbl = tran[height-1][0]
    tranbr = tran[height-1][width-1]
    
    unknown = False
    if vert:
        if trantl == orig[0][width-1]:
            outp.write("The images appear to be flipped horizontally, not vertically.\n")
        elif trantl == orig[height-2][0]:
            outp.write("The images appear to be shifted one pixel up.\n")
        elif tranbr == orig[1][width-1]:
            outp.write("The images appear to be shifted one pixel down.\n")
        else:
            unknown = True
    else:
        if trantl == orig[height-1][0]:
            outp.write("The images appear to be flipped vertically, not horizontally.\n")
        elif trantl == orig[0][width-2]:
            outp.write("The images appear to be shifted one pixel left.\n")
        elif trantr == orig[0][1]:
            outp.write("The images appear to be shifted one pixel right.\n")
        else:
            unknown = True
    
    if unknown:
        count = 0
        for line in tran:
            for pixel in line:
                if pixel.alpha == 0:
                    count += 1
        if count != 1:
            outp.write("The flip operation is not preserving alpha values.\n")
        else:
            outp.write("Compare the incorrect images with the provided solutions.\n")


def comment_transpose(func,options,outp):
    """
    Report specific feedback about a transpose operation
    
    Param func: The filter function
    Precondition: func is a reference to the function 'transpose'
    
    Parameter options: the image options
    Precondition: options is a dictionary
    
    Parameter outp: The output stream
    Precondition: outp is a stream writer
    """
    orig = read_image('blocks.png')
    tran = read_image('blocks.png')
    height = len(orig)
    width  = len(orig[0])
    
    # This would have crashed already
    func(tran,**options)
    trantl = tran[0][0]
    trantr = tran[0][width-1]
    tranbl = tran[height-1][0]
    tranbr = tran[height-1][width-1]
    
    if trantl == orig[0][width-1] and trantr == orig[height-1][width-1]:
        outp.write("The images appear to be rotated left, not transposed.\n")
    elif trantr == orig[0][0] and tranbr == orig[0][width-1]:
        outp.write("The images appear to be rotated right, not transposed.\n")
    elif trantl == orig[0][width-1] and tranbl == orig[height-1][width-1]:
        outp.write("The images appear to flipped horizontally, not transposed.\n")
    elif tranbl == orig[0][0] and tranbr == orig[0][width-1]:
        outp.write("The images appear to flipped vertically, not transposed.\n")
    else:
        count = 0
        for line in tran:
            for pixel in line:
                if pixel.alpha == 0:
                    count += 1
        if count != 1:
            outp.write("The transpose operation is not preserving alpha values.\n")
        else:
            outp.write("Compare the incorrect images with the provided solutions.\n")


def comment_rotate(func,options,outp):
    """
    Report specific feedback about a rotate operation
    
    Param func: The filter function
    Precondition: func is a reference to the function 'rotate'
    
    Parameter options: the image options
    Precondition: options is a dictionary
    
    Parameter outp: The output stream
    Precondition: outp is a stream writer
    """
    orig = read_image('blocks.png')
    tran = read_image('blocks.png')
    height = len(orig)
    width  = len(orig[0])
    
    # This would have crashed already
    func(tran,**options)
    trantl = tran[0][0]
    trantr = tran[0][width-1]
    tranbl = tran[height-1][0]
    tranbr = tran[height-1][width-1]
    
    right = 'right' in options and options['right']
    if trantl == orig[0][0] and tranbl == orig[0][width-1]:
        outp.write("The images appear to be transposed, not rotated.\n")
    elif right and trantl == orig[0][width-1] and trantr == orig[height-1][width-1]:
        outp.write("The images appear to be rotated left, not right.\n")
    elif not right and trantr == orig[0][0] and tranbr == orig[0][width-1]:
        outp.write("The images appear to be rotated right, not left.\n")
    elif trantl == orig[0][width-1] and tranbl == orig[height-1][width-1]:
        outp.write("The images appear to flipped horizontally, not transposed.\n")
    elif tranbl == orig[0][0] and tranbr == orig[0][width-1]:
        outp.write("The images appear to flipped vertically, not transposed.\n")
    else:
        count = 0
        for line in tran:
            for pixel in line:
                if pixel.alpha == 0:
                    count += 1
        if count != 1:
            outp.write("The rotate operation is not preserving alpha values.\n")
        else:
            outp.write("Compare the incorrect images with the provided solutions.\n")
    outp.write("Verify that the error is not in 'flip' or 'transpose'.\n")


pass
#mark -
#mark Graders
def grade_header(file,outp=sys.stdout):
    """
    Grades the file docstring
    
    Parameter name: The file name
    Precondition: name is a string
    
    Parameter outp: The output stream
    Precondition: outp is a stream writer
    """
    status, p1 = grade_docstring(file,1,outp)
    if p1 == 1:
        outp.write('The module docstring looks good.\n\n')
    else:
        outp.write('\n')
    return p1 if not status else None


def grade_part1(file,outp=sys.stdout):
    """
    Grades the first part, the mono functions.
    
    Parameter name: The file name
    Precondition: name is a string
    
    Parameter outp: The output stream
    Precondition: outp is a stream writer
    """
    
    func = 'mono'
    opts = {}
    outp.write("Comments for %s %s:\n" % (repr(func),image_opts(opts)))
    status, p1 = grade_func(file,func,opts,1,outp)
    if p1 == 1:
        outp.write('The function looks good.\n\n')
    else:
        outp.write('\n')
    
    opts = {'sepia':True}
    outp.write("Comments for %s %s:\n" % (repr(func),image_opts(opts)))
    status, p2 = grade_func(file,func,opts,1,outp)
    if p2 == 1:
        outp.write('The function looks good.\n\n')
    else:
        outp.write('\n')

    
    total = round(0.5*p1+0.5*p2,3)
    return total


def grade_part2(file,outp=sys.stdout):
    """
    Grades the second part, the flip functions.
    
    Parameter name: The file name
    Precondition: name is a string
    
    Parameter outp: The output stream
    Precondition: outp is a stream writer
    """
    
    func = 'flip'
    opts = {}
    outp.write("Comments for %s %s:\n" % (repr(func),image_opts(opts)))
    status, p1 = grade_func(file,func,opts,1,outp)
    if p1 == 1:
        outp.write('The function looks good.\n\n')
    else:
        outp.write('\n')
    
    opts = {'vertical':True}
    outp.write("Comments for %s %s:\n" % (repr(func),image_opts(opts)))
    status, p2 = grade_func(file,func,opts,1,outp)
    if p2 == 1:
        outp.write('The function looks good.\n\n')
    else:
        outp.write('\n')

    
    total = round(0.5*p1+0.5*p2,3)
    return total


def grade_part3(file,outp=sys.stdout):
    """
    Grades the thirds part, the rotate functions.
    
    Parameter name: The file name
    Precondition: name is a string
    
    Parameter outp: The output stream
    Precondition: outp is a stream writer
    """
    
    func = 'transpose'
    opts = {}
    outp.write("Comments for %s %s:\n" % (repr(func),image_opts(opts)))
    status, p1 = grade_func(file,func,opts,1,outp)
    if p1 == 1:
        outp.write('The function looks good.\n\n')
    else:
        outp.write('\n')
    
    func = 'rotate'
    outp.write("Comments for %s %s:\n" % (repr(func),image_opts(opts)))
    status, p2 = grade_func(file,func,opts,1,outp)
    if p2 == 1:
        outp.write('The function looks good.\n\n')
    else:
        outp.write('\n')
    
    opts = {'right':True}
    outp.write("Comments for %s %s:\n" % (repr(func),image_opts(opts)))
    status, p3 = grade_func(file,func,opts,1,outp)
    if p3 == 1:
        outp.write('The function looks good.\n\n')
    else:
        outp.write('\n')
    
    total = round(0.4*p1+0.3*p2+0.3*p3,3)
    return total


def grade(outp=sys.stdout):
    """
    Invokes this subgrader (returning a percentage)
    """
    file = 'plugins.py'
    outp.write('Docstring comments:\n')
    p1 = grade_header(file)
    
    if not p1 is None:
        p2 = grade_part1(file)
        p3 = grade_part2(file)
        p4 = grade_part3(file)
    else:
        p1 = 0
        p2 = 0
        p3 = 0
        p4 = 0
    
    total = round(0.05*p1+0.3*p2+0.32*p3+0.33*p4,3)
    return total


if __name__ == '__main__':
    print(grade())