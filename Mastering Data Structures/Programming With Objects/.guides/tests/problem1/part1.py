#!/usr/local/bin/python3
"""
Assess part 1, the first assignment

This file is insecurely available to students, but if they find it and modify it, they
really did not need this course.

Author: Walker M. White
Date:   July 31, 2018
"""
import verifier
import sys


def check_script1(file):
    """
    Checks that the first assignment is correct
    
    Parameter file: The file to check
    Precondition: file is a string
    """
    result = verifier.grade_script(file,0)
    if not result[0]:
        print("The first assignment (and print) looks correct.")
    return result[0]


if __name__ == '__main__':
    sys.exit(check_script1('script.py'))
