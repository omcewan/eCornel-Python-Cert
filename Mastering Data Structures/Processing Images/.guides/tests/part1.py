#!/usr/local/bin/python3
"""
Assess part 1, mono with no options

This file is insecurely available to students, but if they find it and modify it, they
really did not need this course.

Author: Walker M. White
Date:   July 31, 2018
"""
import verifier
import sys


def check_func1(file):
    """
    Checks that the function mono (no options) works correctly
    
    Parameter file: The file to check
    Precondition: file is a string
    """
    func = 'mono'
    opts = {}
    result = verifier.grade_func(file,func,opts,0)
    if not result[0]:
        print("The function %s %s looks correct." % (repr(func),verifier.image_opts(opts)))
    return result[0]


if __name__ == '__main__':
    sys.exit(check_func1('plugins.py'))
