"""
A script asking a user for a number

This script asks the user for a number, and then shows the next one.  It uses
try-except to prevent crashes.

Author: Walker M. White
Date:   April 15, 2019
"""


try:
    result = input('Number: ')      # get the number
    x = float(result)               # convert to float
    print('The next number is '+str(x+1))
except:
    print('That is not a number!')
