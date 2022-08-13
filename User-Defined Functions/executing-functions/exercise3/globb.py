"""  
A module to demonstrate global variables.

Author: YOUR NAME HERE
Date: THE DATE HERE
"""

# The global variable
VAR = 1

def next():
    """
    Returns and increments the value of VAR.
    """
    global VAR
    result = VAR
    VAR += 1
    return result