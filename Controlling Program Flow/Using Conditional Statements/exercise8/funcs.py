"""  
A collection of functions to support the translation of words into Pig Latin.

This module contains two functions.  The first function searchs for the location of the 
first vowel.  The second function uses this as a helper to perform the conversion.

Author: Orlando McEwan
Date: 10/03/2022
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


def pigify(s):
    """
    Returns a copy of s converted to Pig Latin

    Pig Latin is childish encoding of English that adheres to the following rules:

    1.  The vowels are 'a', 'e', 'i', 'o', 'u', as well as any 'y'
        that is not the first letter of a word. All other letters are consonants.

        For example, 'yearly' has three vowels  ('e', 'a', and the last 'y') 
        and three consonants (the first 'y', 'r', and 'l').

    2.  If the English word begins with a vowel, append 'hay' to the end of the word 
        to get the Pig Latin equivalent. For example, 'ask 'askhay' and 'use' becomes 
        'usehay'.

    3.  If the English word starts with 'q', then it must be followed by'u'; move 
        'qu' to the end of the word, and append 'ay'.  Hence 'quiet' becomes
        'ietquay' and 'quay' becomes 'ayquay'.

    4.  If the English word begins with a consonant, move all the consonants up to 
        the first vowel (if any) to the end and add 'ay'.  For example, 'tomato' 
        becomes 'omatotay', 'school' becomes 'oolschay'. 'you' becomes 'ouyay' and 
        'ssssh' becomes 'sssshay'.

    Parameter s: the string to change to Pig Latin
    Precondition: s is a nonempty string with only lowercase letters. If s starts with
    'q', then it starts with 'qu'.
    """
    if first_vowel(s) == 0:
        return s + 'hay'
    elif s[0] == 'q' and s[1] == 'u':
        return s[2:] + 'quay'
    elif first_vowel(s) == -1:
        return s + 'ay'
    else:
        return s[first_vowel(s):] + s[:first_vowel(s)] + 'ay'
