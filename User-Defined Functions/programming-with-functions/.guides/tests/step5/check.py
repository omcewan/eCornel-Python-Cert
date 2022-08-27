#!/usr/local/bin/python3
"""
Assess before final submission.

This file is insecurely available to students, but if they find it and modify it, they
really did not need this course.

Author: Walker M. White
Date:   July 31, 2018
"""
import verifier1
import verifier2
import verifier3
import verifier4
import sys


def check_funcs(file):
    """
    Checks that the functions are all correct
    
    Parameter file: The file to check
    Precondition: file is a string
    """
    result = verifier1.grade_docstring(file,0)
    if not result[0]:
        result = verifier1.grade_func_headers(file,0)
    if not result[0]:
        result = verifier3.grade_matching_parens(file,0)
    if not result[0]:
        result = verifier3.grade_first_in_parens(file,0)
    if not result[0]:
        result = verifier4.grade_matching_parens(file,0)
    if not result[0]:
        result = verifier4.grade_first_in_parens(file,0)
    if not result[0]:
        print("The file %s looks correct." % repr(file))
    return result[0]


def check_tests(file):
    """
    Checks that the test cases are all correct
    
    Parameter file: The file to check
    Precondition: file is a string
    """
    result = verifier1.grade_docstring(file,0)
    if not result[0]:
        result = verifier1.grade_proc_headers(file,0)
    if not result[0]:
        result = verifier1.grade_test_structure(file,0)
    if not result[0]:
        result = verifier2.grade_matching_parens(file,0)
    if not result[0]:
        result = verifier2.grade_first_in_parens(file,0)
    if not result[0]:
        print("The file %s looks correct." % repr(file))
    return result[0]


if __name__ == '__main__':
    if not check_tests('tests.py'):
        sys.exit(check_funcs('funcs.py'))
