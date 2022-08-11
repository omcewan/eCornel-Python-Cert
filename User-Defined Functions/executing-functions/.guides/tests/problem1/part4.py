#!/usr/local/bin/python3
"""
Assess part 4, the second print statement

This file is insecurely available to students, but if they find it and modify it, they
really did not need this course.

Author: Walker M. White
Date:   July 31, 2018
"""
import verifier
import sys


def check_output(file):
    """
    Checks that the module portion is okay.
    
    Parameter file: The file to check
    Precondition: file is a string
    """
    result = verifier.grade_body(file,2)
    if not result[0]:
        print("The second print statement looks correct.")
    return result[0]


if __name__ == '__main__':
    sys.exit(check_output('proc.py'))

