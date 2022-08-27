#!/usr/local/bin/python3
"""
Assess part 3, the asserts for iso_8601

This file is insecurely available to students, but if they find it and modify it, they
really did not need this course.

Author: Walker M. White
Date:   July 31, 2018
"""
import verifier
import sys


def check_step3(file):
    """
    Checks that the first assert statement is correct.
    
    Parameter file: The file to check
    Precondition: file is a string
    """
    result = verifier.grade_iso_8601_assert(file,1)
    if not result[0]:
        print("The assert statements in 'iso_8601' look correct.")
    return result[0]


if __name__ == '__main__':
    sys.exit(check_step3('funcs.py'))
