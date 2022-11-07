#!/usr/local/bin/python3
"""
Assess part 2, the function daytime

This file is insecurely available to students, but if they find it and modify it, they
really did not need this course.

Author: Walker M. White
Date:   July 31, 2018
"""
import verifier
import sys


class HTMLizer(object):
    """
    A delegate class to write to sys.stdout.
    
    This class ensures that all writes tou the output are HTML safe.
    """
    
    def write(self,text):
        """
        Writes the given text to an output stream. 
        
        All text is converted to be HTML safe.
        """
        text = text.replace('&','&amp;')
        text = text.replace('<','&lt;')
        text = text.replace('>','&gt;')
        sys.stdout.write(text)


def check_func2(file):
    """
    Checks that the function daytime works correctly
    
    Parameter file: The file to check
    Precondition: file is a string
    """
    outp = HTMLizer()
    result = verifier.grade_func2(file,0,outp)
    if not result[0]:
        print("The function 'daytime' looks correct.")
    return result[0]


if __name__ == '__main__':
    sys.exit(check_func2('funcs.py'))