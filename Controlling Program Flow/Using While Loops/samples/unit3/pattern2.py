"""
A module showing off the second while-loop pattern.

Here we are using a while-loop that stops when a goal in the specification
is true.

Author: Walker M. White
Date:   April 15, 2019
"""


def prompt(prompt,valid):
    """
    Returns: the choice from a given prompt.
    
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
