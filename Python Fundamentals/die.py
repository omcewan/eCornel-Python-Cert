""" 
A simple die roller

Author: Orlando McEwan
Date: 07/24/2022
"""

import random

first = input("Type the first number: ")
first = int(first)

last = input("Type the last number: ")
last = int(last)

roll = random.randint(first, last)

print('Choosing a number between ' + str(first) + ' and ' + str(last) +'.')
print('The number is ' + str(roll) + '.')