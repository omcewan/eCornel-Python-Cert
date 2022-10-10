"""
A module the plays the game of Pig.

The game of Pig is described here:

https://en.wikipedia.org/wiki/Pig_(dice_game)

This game pits the player against an "AI" opponent.  The AI is very simple.  The
opponent continues to roll as long as the score is less than 20 and banks as soon as
the score crosses this threshold.  The number 20 comes from the probability analysis
of the game.

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
    
    The game pits the player against a single (AI) opponent.  The player goes
    first. The winner is the first person to reach target points.
    
    Parameter target: The target score to win the game
    Precondition: target is an int > 0
    """
    player = 0
    other  = 0
    
    while player < target and other < target:
        print('Current score is player '+str(player)+'; opponent '+str(other)+'.')
        player = player + player_turn()
        if player < target:
            other = other + ai_turn(BANK_STRATEGY)
    
    print('Final score is player '+str(player)+'; opponent '+str(other)+'.')
    if player >= 100:
        print('You reached 100 first. You win!')
    else:
        print('Your opponent reached 100 first. You lose.')


def player_turn():
    """
    Returns a score for a player's turn.
    
    This function rolls the die for the player and gives the player the option
    to roll again or bank.  If the player banks, it returns the final score.
    If the player rolls a 1, the score is 0 and the player loses this turn.
    """
    score = 0
    halted = False
    while not halted:
        roll = random.randint(1,6)
        print('You rolled a '+str(roll)+'.')
        if roll != 1:
            score = score + roll
            response = prompt('Your round total is '+str(score)+'. (R)oll or (B)ank?: ',('R', 'B'))
            halted = (response == 'B')
        else:
            score = 0
            halted = True
    
    if score == 0:
        print('You have busted this round.')
    else:
        print('You have banked '+str(score)+' this round.')
    print()
    
    return score


def prompt(prompt,valid):
    """
    Returns the choice from a given prompt.
    
    This function asks the user a question, and waits for a response.  It checks
    if the response is valid against a list of acceptable answers.  If it is not
    valid, it asks the question again. Otherwise, it returns the player's answer.
    
    Parameter prompt: The question prompt to display to the player
    Precondition: prompt is a string
    
    Parameter valid: The valid reponses
    Precondition: valid is a tuple of strings
    """
    # Ask the question for the first time.
    response = input(prompt)
    
    # Continue to ask while the response is not valid.
    while not (response in valid):
        print('Invalid response.  Answer must be one of '+str(valid))
        print()
        response = input(prompt)
    
    return response


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
    score = 0
    halted = False
    while not halted:
        roll = random.randint(1,6)
        print('Your opponent rolled a '+str(roll)+'.')
        if roll != 1:
            score = score + roll
            halted = score >= goal
        else:
            score = 0
            halted = True
    
    if score == 0:
        print('Your opponent busted this round.')
    else:
        print('Your opponent banked '+str(score)+' this round.')
    print()
    
    return score


# Script code
if __name__ == '__main__':
    play(TARGET_SCORE)
