#!/usr/local/bin/python3
"""
Assess part 1, removing the print statements.

This file is insecurely available to students, but if they find it and modify it, they
really did not need this course.

Author: Walker M. White
Date:   July 31, 2018
"""
import verifier
import sys


def check_body(file):
    """
    Checks that the print statements were removed.
    
    Parameter file: The file to check
    Precondition: file is a string
    """
    result = verifier.grade_body(file,0)
    if not result[0]:
        print("The print statments are removed correctly.")
    return result[0]


if __name__ == '__main__':
    sys.exit(check_body('func.py'))
