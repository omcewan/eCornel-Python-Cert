#!/usr/local/bin/python3
"""
Assess part 2, the return statement.

This file is insecurely available to students, but if they find it and modify it, they
really did not need this course.

Author: Walker M. White
Date:   July 31, 2018
"""
import verifier
import sys


def check_body(file):
    """
    Checks that the full body is okay.
    
    Parameter file: The file to check
    Precondition: file is a string
    """
    result = verifier.grade_body(file,1)
    if not result[0]:
        print("The function body looks correct.")
    return result[0]

if __name__ == '__main__':
    sys.exit(check_body('func.py'))

