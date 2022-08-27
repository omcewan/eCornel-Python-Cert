#!/usr/local/bin/python3
"""
Assess part 1, the initial file

This file is insecurely available to students, but if they find it and modify it, they
really did not need this course.

Author: Walker M. White
Date:   July 31, 2018
"""
import verifier
import sys


def check_func1(file):
    """
    Checks that the function is correct.
    
    Parameter file: The file to check
    Precondition: file is a string
    """
    result = verifier.grade_docstring(file,0)
    if not result[0]:
        result = verifier.grade_func(file,0)
    if not result[0]:
        result = verifier.grade_asserts(file,1)
    if not result[0]:
        print("The function 'second_in_list' appears to be correct.")
    return result[0]


if __name__ == '__main__':
    sys.exit(check_func1('func.py'))
