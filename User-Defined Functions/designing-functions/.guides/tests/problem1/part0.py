#!/usr/local/bin/python3
"""
Assess part 0, the invalid header

This file is insecurely available to students, but if they find it and modify it, they
really did not need this course.

Author: Walker M. White
Date:   July 31, 2018
"""
import verifier
import sys


def check_stub0(file):
    """
    Checks that the function has an invalid header
    
    Parameter file: The file to check
    Precondition: file is a string
    """
    result = verifier.verify_header(file)
    if not result:
        print("The function header looks correct.")
    return result


if __name__ == '__main__':
    sys.exit(check_stub0('func.py'))
