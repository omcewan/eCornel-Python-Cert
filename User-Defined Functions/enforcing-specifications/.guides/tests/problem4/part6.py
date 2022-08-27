#!/usr/local/bin/python3
"""
Assess part 7, the final submission

This file is insecurely available to students, but if they find it and modify it, they
really did not need this course.

Author: Walker M. White
Date:   July 31, 2018
"""
import verifier
import sys


def check_step6(file):
    """
    Checks that  complete submission is correct.
    
    Parameter file: The file to check
    Precondition: file is a string
    """
    result = verifier.grade_get_seconds_assert(file,2)
    if not result[0]:
        result = verifier.grade_get_minutes_assert(file,2)
    if not result[0]:
        result = verifier.grade_get_hours_assert(file,2)
    if not result[0]:
        print("The remaining assert statements look correct.")
    return result[0]


if __name__ == '__main__':
    sys.exit(check_step6('funcs.py'))

