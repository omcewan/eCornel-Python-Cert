#!/usr/local/bin/python3
"""
Assess part 6, the alterations to discover_violations

This file is insecurely available to students, but if they find it and modify it, they
really did not need this course.

Author: Walker M. White
Date:   July 31, 2018
"""
import altverifier
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


def check_func6(package,module):
    """
    Checks that the function discover_violations was modified correctly
    
    Parameter package: The application package
    Precondition: package is a string
    
    Parameter module: The module to grade
    Precondition: module is a string
    """
    outp = HTMLizer()
    result = altverifier.grade_func1(package,module,0,outp)
    if not result[0]:
        print("The modifications to 'discover_violations' look correct.")
    return result[0]


if __name__ == '__main__':
    sys.exit(check_func6('auditor','app.py'))