"""
A script illustrating a while loop.

This script asks the user for a number, and then shows the next one.  It uses
try-except to prevent crashes.  In addition, it will ask the user again if the
number is not valid.

Author: Walker M. White
Date:   April 15, 2019
"""


loop = True
while loop:
    try:
        result = input('Number: ')      # get the number
        x = float(result)               # convert to float
        print('The next number is '+str(x+1))
        loop = False
    except:
        print('That is not a number! Try again')
