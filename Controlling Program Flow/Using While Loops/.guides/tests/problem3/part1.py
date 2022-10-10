#!/usr/local/bin/python3
"""
Assess part 1, the function skip

This file is insecurely available to students, but if they find it and modify it, they
really did not need this course.

Author: Walker M. White
Date:   July 31, 2018
"""
import verifier
import sys


def check_func1(file):
    """
    Checks that the function skip works correctly
    
    Parameter file: The file to check
    Precondition: file is a string
    """
    result = verifier.grade_func1(file,0)
    if not result[0]:
        result = verifier.grade_structure(file,'skip',0)
    if not result[0]:
        print("The function 'skip' looks correct.")
    return result[0]


if __name__ == '__main__':
    sys.exit(check_func1('funcs.py'))
