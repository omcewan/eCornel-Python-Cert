#!/usr/local/bin/python3
"""
Assess part 6, the remaining assert statements

This file is insecurely available to students, but if they find it and modify it, they
really did not need this course.

Author: Walker M. White
Date:   July 31, 2018
"""
import verifier
import sys


def check_step7(file):
    """
    Checks that the remaining assert statements are correct.
    
    Parameter file: The file to check
    Precondition: file is a string
    """
    result = verifier.grade_docstring(file,0)
    if not result[0]:
        result = verifier.grade_iso_8601(file,0)
    if not result[0]:
        result = verifier.grade_get_seconds(file,0)
    if not result[0]:
        result = verifier.grade_get_minutes(file,0)
    if not result[0]:
        result = verifier.grade_get_hours(file,0)
    if not result[0]:
        result = verifier.grade_str_to_seconds(file,0)
    if not result[0]:
        result = verifier.grade_str_to_seconds_assert(file,3)
    if not result[0]:
        result = verifier.grade_iso_8601_assert(file,1)
    if not result[0]:
        result = verifier.grade_get_seconds_assert(file,2)
    if not result[0]:
        result = verifier.grade_get_minutes_assert(file,2)
    if not result[0]:
        result = verifier.grade_get_hours_assert(file,2)
    if not result[0]:
        print("The module 'funcs' looks correct.")
    return result[0]


if __name__ == '__main__':
    sys.exit(check_step7('funcs.py'))

