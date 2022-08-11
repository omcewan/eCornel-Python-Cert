#!/usr/local/bin/python3
"""
Assess part 1, replacing first code segment

This file is insecurely available to students, but if they find it and modify it, they
really did not need this course.

Author: Walker M. White
Date:   July 31, 2018
"""
import verifier
import sys


def check_player1(file):
    """
    Checks that the first player was refactored.
    
    Parameter file: The file to check
    Precondition: file is a string
    """
    result = verifier.grade_player1(file,0)
    if not result[0]:
        print("The function call for player 1 looks correct.")
    return result[0]


if __name__ == '__main__':
    sys.exit(check_player1('game.py'))
