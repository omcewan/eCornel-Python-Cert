"""
A script to show off the creation and use of objects.

Author: Orlando McEWan
Date: 10/15/2022
"""
import introcs
import funcs


# Step 1: Create a green RGB object, assign it to variable green, and then print it
green = introcs.RGB(0,255,0,255)
print(green)
# Step 2: Create a 50% transparent red RGB object, assign it to variable red, and print it
red = introcs.RGB(255,0,0,128)
print(red)
# Step 3: Call the function blend on red/green, assign it to variable brown, and print it
brown = funcs.blend(red,green)
print(brown)
# Step 4: Call the function blendUnder on green/red, and then print variable green
funcs.blendUnder(green, red)
print(green)