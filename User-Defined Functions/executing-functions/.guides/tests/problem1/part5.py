#!/usr/local/bin/python3
"""
Assess part 4, right before submission

This file is insecurely available to students, but if they find it and modify it, they
really did not need this course.

Author: Walker M. White
Date:   July 31, 2018
"""
import verifier
import sys


def check_module(file):
    """
    Checks that the module looks okay
    
    Parameter file: The file to check
    Precondition: file is a string
    """
    result = verifier.grade_docstring(file,0)
    if not result[0]:
        print("The module docstring looks correct.")
        result = verifier.grade_header(file,0)
    if not result[0]:
        print("The function header (and docstring) looks correct.")
        result = verifier.grade_body(file,2)
    if not result[0]:
        print("The print statements look correct.")
    return result[0]

if __name__ == '__main__':
    sys.exit(check_module('proc.py'))
