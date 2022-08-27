#!/usr/local/bin/python3
"""
Assess part 4, the initial asserts for str_to_seconds

This file is insecurely available to students, but if they find it and modify it, they
really did not need this course.

Author: Walker M. White
Date:   July 31, 2018
"""
import verifier
import sys


def check_step4(file):
    """
    Checks that the second assert statement is correct.
    
    Parameter file: The file to check
    Precondition: file is a string
    """
    result = verifier.grade_str_to_seconds_assert(file,1)
    if not result[0]:
        print("The initial assert statements in 'str_to_seconds' look correct.")
    return result[0]


if __name__ == '__main__':
    sys.exit(check_step4('funcs.py'))
