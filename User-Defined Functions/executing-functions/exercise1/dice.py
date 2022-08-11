"""  
A module to roll two dice

Author: Walker M. White
Date: January 20, 2019
"""
import random
first = input('Type the first number: ')
last  = input('Type the last number: ')
first = int(first)
last  = int(last)
print('Choosing two numbers between '+str(first)+' and '+str(last)+'.')

# Generate two numbers, add, and print the result
num1 = random.randint(first,last)
num2 = random.randint(first,last)
thesum = num1+num2
print('The sum is '+str(thesum)+'.')
