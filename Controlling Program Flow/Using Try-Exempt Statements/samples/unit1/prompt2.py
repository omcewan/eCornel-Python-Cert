"""
A simple application to query for a number

This is still not robust.  It will crash on bad input

Author: Walker M. White
Date:   March 30, 2019
"""


def is_number(s):
    """
    Returns True if the string s can be cast to a float

    Parameter s: The string to test
    Precondition: s is a string
    """
    # No idea how to implement this
    pass


def main():
    """
    Ask the user for a number and display the 'next one'
    """
    result = input('Number: ')          # get number from user
    if is_number(result):
        x = float(result)               # convert string to float
        print('The next number is '+str(x+1))
    else:
        print('That is not a number')


# Script code
main()
