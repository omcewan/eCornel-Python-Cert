#!/usr/local/bin/python3
"""
Assess part 1, file creation

This file is insecurely available to students, but if they find it and modify it, they
really did not need this course.

Author: Walker M. White
Date:   July 31, 2018
"""
import verifier
import sys


def check_step1(*files):
    """
    Checks that the files are properly created
    
    Parameter file: The files to check
    Precondition: files is list of strings
    """
    result = [0,0]
    for item in files:
        if not result[0]:
            result = verifier.grade_docstring(item,0)
    if not result[0]:
        print("The files %s look correct." % ', '.join(map(repr,files)))
    return result[0]


if __name__ == '__main__':
    sys.exit(check_step1('funcs.py','tests.py'))
