#!/usr/local/bin/python3
"""
Assess part 2, function stubs

This file is insecurely available to students, but if they find it and modify it, they
really did not need this course.

Author: Walker M. White
Date:   July 31, 2018
"""
import verifier
import sys


def check_step2(file):
    """
    Checks that the function stubs are properly created
    
    Parameter file: The file to check
    Precondition: file is a string
    """
    result = verifier.grade_func_headers(file,1)
    if not result[0]:
        print("The function stubs for %s look correct." % repr(file))
    return result[0]


if __name__ == '__main__':
    sys.exit(check_step2('funcs.py'))
