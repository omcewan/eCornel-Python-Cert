"""
Module showing off cross-platform directory handling

This module shows how to use os.path to create a path to a file in a way that
works on both Windows and Unix (MacOS, Linux) systems.

Author: Walker M. White
Date:   June 7, 2019
"""
# Module to navigate directories
import os.path


def read_file(directory,file):
    """
    Returns the contents of file in the given directory.

    Parameter directory: The directory/folder containing the file
    Precondition: directory is a string refering to a directory,
    and that directory contains file

    Parameter file: The file to be read
    Precondition: file is a string refering to a text file, and
    and that file is in directory
    """
    #path = directory + '/' + file
    path = os.path.join(directory, file)
    file = open(path)
    result = file.read()
    file.close()
    return result
