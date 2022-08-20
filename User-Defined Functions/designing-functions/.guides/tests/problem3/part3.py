#!/usr/local/bin/python3
"""
Assess part 1, the function with a stubbed result.

This file is insecurely available to students, but if they find it and modify it, they
really did not need this course.

Author: Walker M. White
Date:   July 31, 2018
"""
import verifier
import sys


def check_stub1(file):
    """
    Checks that the function result is returned correctly
    
    Parameter file: The file to check
    Precondition: file is a string
    """
    result = verifier.grade_docstring(file,0)
    result = result[0]
    if not result:
        result = verifier.verify_result(file,0)
    if not result:
        print("The return step looks correct.")
    return result


if __name__ == '__main__':
    sys.exit(check_stub1('func.py'))
