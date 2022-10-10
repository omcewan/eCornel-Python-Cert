#!/usr/local/bin/python3
"""
Assess part 7, before submission

This file is insecurely available to students, but if they find it and modify it, they
really did not need this course.

Author: Walker M. White
Date:   July 31, 2018
"""
import verifier
import sys


def check_func7(file):
    """
    Checks that the test cases are correct
    
    Parameter file: The file to check
    Precondition: file is a string
    """
    result = verifier.grade_func1(file,1)
    if not result[0]:
        result = verifier.grade_structure(file,'flips',0)
    if not result[0]:
        result = verifier.grade_func2(file,1)
    if not result[0]:
        result = verifier.grade_structure(file,'partition',0)
    if not result[0]:
        print("Both functions appear to be correct.")
    return result[0]


if __name__ == '__main__':
    sys.exit(check_func7('funcs.py'))
