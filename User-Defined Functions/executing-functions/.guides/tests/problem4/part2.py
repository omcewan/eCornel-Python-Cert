#!/usr/local/bin/python3
"""
Assess part 2, the second player

This file is insecurely available to students, but if they find it and modify it, they
really did not need this course.

Author: Walker M. White
Date:   July 31, 2018
"""
import verifier
import sys


def check_player2(file):
    """
    Checks that the second player was refactored.
    
    Parameter file: The file to check
    Precondition: file is a string
    """
    result = verifier.grade_player2(file,0)
    if not result[0]:
        print("The function call for player 2 looks correct.")
    return result[0]

if __name__ == '__main__':
    sys.exit(check_player2('game.py'))

