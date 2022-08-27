#!/usr/local/bin/python3
"""
Assess part 3, before moving on to the next step.

This file is insecurely available to students, but if they find it and modify it, they
really did not need this course.

Author: Walker M. White
Date:   July 31, 2018
"""
import verifier
import sys


def check_step3(file):
    """
    Checks that the test cases are all correct
    
    Parameter file: The file to check
    Precondition: file is a string
    """
    result = verifier.grade_matching_parens(file,0)
    if not result[0]:
        result = verifier.grade_first_in_parens(file,0)
    if not result[0]:
        print("The test cases for %s all look correct." % repr(file))
    return result[0]


if __name__ == '__main__':
    sys.exit(check_step3('tests.py'))
