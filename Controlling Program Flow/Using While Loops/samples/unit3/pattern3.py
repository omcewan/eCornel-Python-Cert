"""
A module showing off the third while-loop pattern.

Here we are using a while-loop with an explicit boolean loop variable. The body
sets the variable to False when it is time to stop.

Author: Walker M. White
Date:   April 15, 2019
"""
import random


def roll_past(goal):
    """
    Returns: The score from rolling a die until passing goal.
    
    This function starts with a score of 0, and rolls a die, adding the
    result to the score.  Once the score passes goal, it stops and
    returns the result as the final score.
    
    If the function ever rolls a 1, it stops and the score is 0.
    
    Parameter goal: The target goal to hit
    Precondition: goal is an int > 0
    """
    score = 0
    loop = True
    while loop:
        roll = random.randint(1,6)
        if roll == 1:
            score = 0
            loop = False
        else:
            score = score + roll
            loop = score < goal
    
    return score
