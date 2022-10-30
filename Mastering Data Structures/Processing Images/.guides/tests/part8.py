#!/usr/local/bin/python3
"""
Assess part 8, before submission (mono)

This file is insecurely available to students, but if they find it and modify it, they
really did not need this course.

Author: Walker M. White
Date:   July 31, 2018
"""
import verifier
import sys


def check_func8(file):
    """
    Checks that the test cases are correct
    
    Parameter file: The file to check
    Precondition: file is a string
    """
    func = 'mono'
    opts = {'sepia':True}
    result = verifier.grade_docstring(file,0)
    if not result[0]:
        result = verifier.grade_func(file,func,{},0)
    if not result[0]:
        result = verifier.grade_func(file,func,opts,0)
    if not result[0]:
        print("The 'mono' operations look correct.")
    return result[0]


if __name__ == '__main__':
    sys.exit(check_func8('plugins.py'))
