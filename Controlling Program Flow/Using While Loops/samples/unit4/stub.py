"""
A module the plays the game of Pig.

The game of Pig is described here:

https://en.wikipedia.org/wiki/Pig_(dice_game)

This version contains function stubs to help us design.

Author: Walker M. White
Date:   April 15, 2019
"""
import random


# The goal to play towards
TARGET_SCORE  = 100
# The bank strategy for the AI player
BANK_STRATEGY = 20


def play(target):
    """
    Plays a single game of Pig to target score.

    The game pits the player against a single (AI) opponent.  The player goes first.
    The winner is the first person to reach target points.

    Parameter target: The target score to win the game
    Precondition: target is an int > 0
    """
    # Initialize the scores
    # while no one has reached the target
        # Play a round for the player
        # If the player did not reach the target
              # Play a round for the opponent (primitive AI)
    # Display the results


def player_turn():
    """
    Returns a score for a player's turn.

    This function rolls the die for the player and gives the player the option
    to roll again or bank.  If the player banks, it returns the final score.
    If the player rolls a 1, the score is 0 and the player loses this turn.
    """
    # while the player has not stopped
        # Roll the die
        # If is a 1
              # Set score to 0 and stop the turn
        # else
              # Add that to the score
              # Ask the player whether to continue
    # Return the score


def ai_turn(goal):
    """
    Returns the score for the opponent's turn.

    This function rolls the die for the opponent, and adds the value to the turn
    score. Using a primitive Pig strategy, the opponent keeps rolling until the
    score meets or exceeds goal. If the opponent ever rolls a 1, the score is 0
    and the opponent loses this turn.

    Parameter goal: The target goal to hit this turn
    Precondition: goal is an int > 0
    """
    # while ai has not reached goal
        # Roll the die
        # If is a 1
              # Set score to 0 and stop the turn
        # else
              # Add that to the score
    # Return the score
















# Script code
if __name__ == '__main__':
    play(TARGET_SCORE)
