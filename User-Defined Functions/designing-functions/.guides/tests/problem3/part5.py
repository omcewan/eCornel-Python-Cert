#!/usr/local/bin/python3
"""
Assess part 3, the function with slicing

This file is insecurely available to students, but if they find it and modify it, they
really did not need this course.

Author: Walker M. White
Date:   July 31, 2018
"""
import verifier
import sys


def check_stub3(file):
    """
    Checks that the function result is sliced correctly
    
    Parameter file: The file to check
    Precondition: file is a string
    """
    result = verifier.verify_slice(file)
    if not result:
        print("The string appears to be sliced correctly.")
    return result


if __name__ == '__main__':
    sys.exit(check_stub3('func.py'))
