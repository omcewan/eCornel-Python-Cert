#!/usr/local/bin/python3
"""
Assess part 2, the remaining test cases

This file is insecurely available to students, but if they find it and modify it, they
really did not need this course.

Author: Walker M. White
Date:   July 31, 2018
"""
import verifier
import sys


def check_func2(file):
    """
    Checks that the test cases are correct
    
    Parameter file: The file to check
    Precondition: file is a string
    """
    result = verifier.grade_testcases(file,1)
    if not result[0]:
        print("There appear to be at least 10 different test cases.")
    return result[0]


if __name__ == '__main__':
    sys.exit(check_func2('test.py'))