"""
A simple application to query for a number

This version is not robust.  It will crash on bad input

Author: Walker M. White
Date:   March 30, 2019
"""


def main():
    """
    Ask the user for a number and display the 'next one'
    """
    result = input('Number: ')          # get number from user
    x = float(result)                   # convert string to float
    print('The next number is '+str(x+1))


# Script code
main()
