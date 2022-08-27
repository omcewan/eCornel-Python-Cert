#!/usr/local/bin/python3
"""
Assess part 2, implementation of first_in_parens

This file is insecurely available to students, but if they find it and modify it, they
really did not need this course.

Author: Walker M. White
Date:   July 31, 2018
"""
import verifier
import sys


def check_step2(file):
    """
    Checks that first_in_parens is implemented correctly
    
    Parameter file: The file to check
    Precondition: file is a string
    """
    result = verifier.grade_first_in_parens(file,0)
    if not result[0]:
        print("The function 'first_in_parens' looks correct.")
    return result[0]


if __name__ == '__main__':
    sys.exit(check_step2('funcs.py'))
