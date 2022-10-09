"""
A simple application to query for a number

This is version is robust and should not crash.

Author: Walker M. White
Date:   March 30, 2019
"""


def main():
    """
    Ask the user for a number and display the 'next one'
    """
    try:
        result = input('Number: ')      # get number from user
        x = float(result)               # convert string to float
        print('The next number is '+str(x+1))
    except:
        print('That is not a number')


# Script code
main()
