"""
A module showing off the first while-loop pattern.

Here we are using a while-loop to replace a range computation.

Author: Walker M. White
Date:   April 15, 2019
"""


def count_slash_for(s):
    """
    Returns the number of times '/' appears in string s
    
    Parameter s: the string to search
    Precondition: s is a (possibly empty) string
    """
    # Accumulator
    count = 0
    
    # Loop variable
    for i in range(len(s)):
        if s[i] == '/':
            count= count + 1
    
    return count


def count_slash_while(s):
    """
    Returns the number of times '/' appears in string s
    
    Parameter s: the string to search
    Precondition: s is a (possibly empty) string
    """
    # Accumulator
    count = 0
    
    # Loop variable
    i = 0
    while i < len(s):
        if s[i] == '/':
            count= count + 1
        i= i + 1
    
    return count


def add_fracs_for(n):
    """
    Returns the sum of the fractions 1/1 + 1/2 + ... + 1/n
    
    Parameter n: The number of fractions to add
    Precondition: n is an int > 0
    """
    # Accumulator
    v = 0           # call this 1/0 for today
    
    for i in range(1,n+1):
        v = v + 1.0 / i
    
    return v


def add_fracs_while(n):
    """
    Returns the sum of the fractions 1/1 + 1/2 + ... + 1/n
    
    Parameter n: The number of fractions to add
    Precondition: n is an int > 0
    """
    # Accumulator
    v = 0           # call this 1/0 for today
    
    # Loop variable
    i = 1
    while i <= n:
        v = v + 1.0 / i
        i = i + 1
    
    return v
