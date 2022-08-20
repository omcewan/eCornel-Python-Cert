#!/usr/local/bin/python3
"""
Assess part 2, the function with trimming

This file is insecurely available to students, but if they find it and modify it, they
really did not need this course.

Author: Walker M. White
Date:   July 31, 2018
"""
import verifier
import sys


def check_stub2(file):
    """
    Checks that the function result is trimmed correctly
    
    Parameter file: The file to check
    Precondition: file is a string
    """
    result = verifier.verify_result(file,1)
    if not result:
        print("The return value is trimmed correctly.")
    return result


if __name__ == '__main__':
    sys.exit(check_stub2('func.py'))
