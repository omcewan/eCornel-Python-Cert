#!/usr/local/bin/python3
"""
Assess part 3, the test cases

This file is insecurely available to students, but if they find it and modify it, they
really did not need this course.

Author: Walker M. White
Date:   July 31, 2018
"""
import verifier
import sys


def check_func3(file):
    """
    Checks that the function test cases are correct.
    
    Parameter file: The file to check
    Precondition: file is a string
    """
    result = verifier.grade_testcases(file,0)
    if not result[0]:
        print("The test cases look correct.")
    return result[0]


if __name__ == '__main__':
    sys.exit(check_func3('test.py'))
