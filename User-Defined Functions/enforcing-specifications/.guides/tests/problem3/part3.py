#!/usr/local/bin/python3
"""
Assess part 3, the error message

This file is insecurely available to students, but if they find it and modify it, they
really did not need this course.

Author: Walker M. White
Date:   July 31, 2018
"""
import verifier
import sys


def check_func3(file):
    """
    Checks that the function is complete.
    
    Parameter file: The file to check
    Precondition: file is a string
    """
    result = verifier.grade_messages(file,1)
    if not result[0]:
        print("The second error message appears to be correct.")
    return result[0]


if __name__ == '__main__':
    sys.exit(check_func3('func.py'))
