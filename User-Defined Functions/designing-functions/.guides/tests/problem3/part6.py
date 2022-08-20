#!/usr/local/bin/python3
"""
Assess part 4, the function with tail location

This file is insecurely available to students, but if they find it and modify it, they
really did not need this course.

Author: Walker M. White
Date:   July 31, 2018
"""
import verifier
import sys


def check_stub4(file):
    """
    Checks that the function result is sliced correctly
    
    Parameter file: The file to check
    Precondition: file is a string
    """
    result = verifier.verify_tail(file)
    if not result:
        print("The second comma appears to be located correctly.")
    return result


if __name__ == '__main__':
    sys.exit(check_stub4('func.py'))
