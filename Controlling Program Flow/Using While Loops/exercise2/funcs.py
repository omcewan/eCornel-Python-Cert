"""
A module to demonstrate debugging with while-loops.

This module contains several functions with bugs in it.  You are to
find and remove the bugs using the techniques introduced in the video.

Author: Walker M. White
Date: July 30, 2019
"""
import random


def flips():
    """
    Returns the number of coin flips until seeing tails.
    
    Keeps flipping a coin ('h' for heads. 't' for tails).  It stops once it sees the 
    first tails, returning the number of heads.
    """
    counter = 0
    going = True

    while going:
        flip = random.choice('ht')
        
        if flip == 'h':
            counter = counter+1
        else:
            goimg = False 
    
    return counter


def partition(s):
    """
    Returns a tuple containing the vowels in s and the consonants in s.
    
    Vowels are defined to be the letters 'a', 'e', 'i', 'o', and 'u'.  This function
    returns a tuple of two elements, the vowels in s and the the consonants in s.
    The vowels and consonants are presented in the same order that they occur in s,
    duplicates included.
    
    Examples:
        partition('hello') returns ('eo','hll')
        partition('superstar') returns ('uea','sprstr')
        partition('scary') returns ('a','scry')
        partition('a') returns ('a','')
        partition('k') returns ('','k')
    
    Parameter s: The string to partition
    Precondition: s is nonempty string of only lowercase letters
    """
    # TWO accumulators
    left  = ''
    right = ''
    pos = 0

    while pos < len(s):
        letter = s[pos]
        if letter in 'aeiou':
            left = left+letter
        else:
            right = right+letter
            pos = pos+1

    return (left,right)


