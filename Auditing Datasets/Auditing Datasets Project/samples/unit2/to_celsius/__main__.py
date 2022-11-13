"""
Application code to convert farenheit to celsius.

This application prompts the user for a number representing degrees in farenheit. It then
prints out the equivalent degrees in celsius.

Author: Walker M. White (wmw2)
Date:   June 7, 2019
"""
import temp

try:
    data = input("Degrees farenheit: ")
    data = float(data)
    result = temp.to_celsius(data)
    
    # Round it to make it look pretty when we print
    result = round(result,2)
    print(str(data)+' degrees farenheit is '+str(result)+' degrees celsius.')
except:
    # Recover if we got bad input
    print('That is not a valid input.')