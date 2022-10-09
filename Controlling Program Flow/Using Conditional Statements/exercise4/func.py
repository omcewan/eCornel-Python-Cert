"""  
A function to search for the first vowel position

Author: Orlando McEwan
Date: 09/27/2022
"""
import introcs


def first_vowel(s):
    """
    Returns the position of the first vowel in s; it returns -1 if there are no vowels.
    
    We define the vowels to be the letters 'a','e','i','o', and 'u'.  The letter
    'y' counts as a vowel only if it is not the first letter in the string.
    
    Examples: 
        first_vowel('hat') returns 1
        first_vowel('grrm') returns -1
        first_vowel('sky') returns 2
        first_vowel('year') returns 1
    
    Parameter s: the string to search
    Precondition: s is a nonempty string with only lowercase letters
    """
    result = len(s)

    # find the index for every vowel if it exists
    vowel_a = introcs.find_str(s, 'a')
    vowel_e = introcs.find_str(s, 'e')
    vowel_i = introcs.find_str(s, 'i')
    vowel_o = introcs.find_str(s, 'o')
    vowel_u = introcs.find_str(s, 'u')
    vowel_y = introcs.find_str(s, 'y', 1)

    # use if statments to check which vowel has the smallest index.
    if vowel_a < result and vowel_a > -1:
        result = vowel_a

    if vowel_e < result and vowel_e > -1:
        result = vowel_e

    if vowel_i < result and vowel_i > -1:
        result = vowel_i

    if vowel_o < result and vowel_o > -1:
        result = vowel_o

    if vowel_u < result and vowel_u > -1:
        result = vowel_u

    if vowel_y < result and vowel_y > -1:
        result = vowel_y

    return -1 if result == len(s) else result 