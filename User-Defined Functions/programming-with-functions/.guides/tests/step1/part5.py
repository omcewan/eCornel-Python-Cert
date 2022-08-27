#!/usr/local/bin/python3
"""
Assess part 5, before moving on to the next step.

This file is insecurely available to students, but if they find it and modify it, they
really did not need this course.

Author: Walker M. White
Date:   July 31, 2018
"""
import verifier
import sys


def check_step5(*files):
    """
    Checks that the files are all correct
    
    Parameter file: The files to check
    Precondition: files is list of strings, the function file being first
    """
    result = [0,0]
    for item in files:
        if not result[0]:
            result = verifier.grade_docstring(item,0)
    if not result[0]:
        result = verifier.grade_func_headers(files[0],0)
    if not result[0]:
        result = verifier.grade_proc_headers(files[1],0)
    if not result[0]:
        result = verifier.grade_test_structure(files[1],0)
    if not result[0]:
        print("The files %s look correct." % ', '.join(map(repr,files)))
    return result[0]


if __name__ == '__main__':
    sys.exit(check_step5('funcs.py','tests.py'))
