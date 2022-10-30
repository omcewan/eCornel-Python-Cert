"""
Application for processing images.

This application contains the core code for reading and saving images, as well as
processing the command line arguments. While there is a bit of advanced code in this 
file, you have learned enough Python by now to be able to understand a lot 
(but not all) of this file. 

One of the most advanced things in this file is the use of the functions hasattr 
and getattr. These allow us to treat a module like a dictionary, checking for the 
presence of a function and then retrieving the function by name.  This is how we 
support the plug-in features of this application.

This function also supports processing of command line arguments. This is made
possible by the sys module built into Python.

Finally, this function makes use of the module PIL which was installed when you
installed introcs.  Its documentation can be found here:
    
    https://pillow.readthedocs.io/en/stable/reference/Image.html

With that said, it is not a problem if you do not understand the code in this file.
It is very possible to do the project without it, and this project was written
assuming that you would not even read this docstring.

Author: Walker M. White
Date: August 11, 2019
"""
from PIL import Image as CoreImage
import traceback
import introcs
import os.path
import plugins
import sys


# The number of periods in the "progress bar"
PROGRESS = 10


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
        image = CoreImage.open(file)
        print(('Loading ' + repr(file)),end='',flush=True)
        
        # Extract data from PIL
        image = image.convert("RGBA")
        width  = image.size[0]
        height = image.size[1]
        
        # Poor man's progress bar
        size = width*height
        block = max(size//PROGRESS,1)
        
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
                
                # Update progress bar every block steps
                if (r*width+c) % block == 0:
                    print('.',end='',flush=True)
            
            buffer.append(row)
        
        print('done')
        return buffer
    except:
        # This displays error message even though we are not technically crashing
        traceback.print_exc()
        print('Could not load the file ' + repr(file))
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
        return False
    
    width = len(first)
    for row in buffer:
        if len(row) != width:
            return False
        for item in row:
            if type(item) != introcs.RGB:
                return False
    
    return True


def save_image(buffer,file):
    """
    Saves the given image buffer to the specified file.
    
    If the image cannot be written (image is corrupt, file name is invalid, etc.)
    this function will display an error message. Otherwise this function prints out 
    a simple progress bar to indicate how far along it is in saving. The progress bar 
    consists of several periods followed by 'done'.
    
    Parameter buffer: The image buffer to save
    Precondition: buffer is a 2d table of RGB objects
    
    Parameter file: The file name to save to
    Precondition: file is a string
    """
    # Make sure the student did not damage anything
    assert verify_image(buffer), 'A plug-in has corrupted the image data'
    try:
        height = len(buffer)
        width  = len(buffer[0])
        
        # Poor man's progress bar
        size = width*height
        block = max(size//PROGRESS,1)
        
        print(('Saving ' + repr(file)),end='',flush=True)
        im = CoreImage.new('RGBA',(width,height))
        
        # Convert student data back to PIL format
        output = []
        for r in range(height):
            for c in range(width):
                pixel = buffer[r][c]
                output.append(pixel.rgba())
                
                # Update progress bar every block steps
                if (r*width+c) % block == 0:
                    print('.',end='',flush=True)
        im.putdata(output)
        
        im.save(file,'PNG')
        print('done')
    except:
        # This displays error message even though we are not technically crashing
        traceback.print_exc()
        print('Could not save the file ' + repr(file))


def parse_args(args):
    """
    Returns a dictionary interpreting the command line arguments.
    
    If there is an error in parsing, the returned dictionary will have the key 'error'
    refering to an error message.  Otherwise, the dictionary will contain the 
    (1) plugin function, (2) the optional arguments to the plug-in function, and
    (3) the input file.  It will also contain the output file if specified.
    
    In addition to returning the argument dictionary, this function modifies args
    to remove all options from it.  So it is not a good idea to call this function
    directly on sys.argv.
    
    Parameter args: The command line arguments
    Precondition: args is a list of strings
    """
    # Strip out options
    options = extract_options(args)
    result = {}
    usage = 'usage: python3 pictool.py command [options] input [output]'
    if not len(args) in [3,4]:
        result['error'] = usage
    else:
        command = lookup_command(args[1],options)
        if type(command) == str:
            result['error'] = command
        else:
            result['command'] = command
            result['options'] = options
        
        result['input'] = args[2]
        if len(args) == 4:
            result['output'] = args[3]
    
    return result


def lookup_command(command,options):
    """
    Returns the function in plugins matching command, or an error message if not found.
    
    The function looks for a function in plugins with the name of command.  It also 
    makes sure that this function has the proper signature (first parameter image,
    all later parameters optional).  If optional is not empty, it verifies that the
    keys of optional refer to valid parameters of the function.
    
    If there are any problems (function not found, options do not match), this function
    returns a string with the specific error message.
    
    Parameter command: The function name
    Precondition: command is a string
    
    Parameter options: The function arguments
    Precondition: options is a dictionary
    """
    if not hasattr(plugins,command):
        return 'error: unrecognized command '+repr(command)
    
    error = None
    function = getattr(plugins,command)
    param = function.__code__.co_varnames[:function.__code__.co_argcount]
    dsize = 0 if function.__defaults__ is None else len(function.__defaults__)
    if len(param) != dsize+1:
        error = 'error: plugin '+repr(command)+' does not have default values after first parameter'
    else:
        badargs = []
        for key in options:
            if not key in param:
                badargs.append(key)
        if badargs:
            flags = ', '.join(map(lambda x : '--'+x,badargs))
            error = 'error: plugin '+repr(command)+' does not recognize the following options: '+flags
    
    return function if error is None else error


def extract_options(args):
    """
    Extracts the optional arguments from the command line arguments.
    
    An optional argument is any that starts with '--' and has the form 'name=value'.
    This function returns this arguments as a dictionary name:value pairs.  In 
    addition, values are converted to Python types (boolean, int, float) whenever
    possible.
    
    In addition to returning the dictionary of options, this function modifies args
    to remove all options from it.  So it is not a good idea to call this function
    directly on sys.argv.
    
    Parameter args: The command line arguments
    Precondition: args is a list of strings
    """
    options = {}
    pos = 1
    while pos < len(args):
        item = args[pos]
        if item.startswith('--') and '=' in item:
            split = item.find('=')
            value = item[split+1:]
            
            # Convert value to a Python type, if possible
            if value in ['True','False']:
                value = eval(value)
            elif value.isdigit():
                value = int(value)
            else:
                try:
                    value = float(value)
                except:
                    pass
        
            options[item[2:split]] = value
            del args[pos]
        else:
            pos = pos+1
    
    return options


def main():
    """
    Runs the image processing tool.
    
    This function parses the command line arguments to (1) load a file, (2) process it
    and (3) save it when appropriate.
    """
    import datetime
    args = parse_args(sys.argv[:])
    if 'error' in args:
        print(args['error'])
        return
    
    buffer = read_image(args['input'])
    if buffer is None:
        return
    
    start = datetime.datetime.now()
    print('Processing '+repr(args['input']),end='',flush=True)
    process = args['command'](buffer,**args['options'])
    print('..done')
    end = datetime.datetime.now()
    # Uncomment this to see how long it is taking to process images
    print('Time: '+str(end-start)) 
    if process and 'output' in args:
        save_image(buffer,args['output'])


# Script code
if __name__ == '__main__':
    main()
