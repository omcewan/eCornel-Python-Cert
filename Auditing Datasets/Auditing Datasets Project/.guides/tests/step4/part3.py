#!/usr/local/bin/python3
"""
Assess part 3, before submission

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


def check_final(package,module):
    """
    Checks that the module is correct
    
    Parameter package: The application package
    Precondition: package is a string
    
    Parameter module: The module to grade
    Precondition: module is a string
    """
    outp = HTMLizer()
    functions = ['func1','func2']
    result = verifier.grade_docstring(package,module,0,outp)
    for item in functions:
        if not result[0]:
            func = getattr(verifier,'grade_'+item)
            result = func(package,module,0,outp)
    if not result[0]:
        print("All of the functions look correct.")
    return result[0]

if __name__ == '__main__':
    sys.exit(check_final('auditor','app.py'))
