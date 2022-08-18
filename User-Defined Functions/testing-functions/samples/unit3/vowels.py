"""
A module with a well-specified function

Author: Walker M. White
Date:   February 14, 2019
"""
import introcs


def number_vowels(w):
    """
    Returns: number of vowels in string w.

    Vowels are defined to be 'a','e','i','o', and 'u'. 'y' is a vowel if it is
    not at the start of the word.

    Repeated vowels are counted separately. Both upper case and lower case
    vowels are counted.

    Examples:
        number_vowels('hat') returns 1
        number_vowels('hate') returns 2
        number_vowels('beet') returns 2
        number_vowels('sky') returns 1
        number_vowels('year') returns 2
        number_vowels('xxx') returns 0

    Parameter w: The text to check for vowels
    Precondition: w string w/ at least one letter and only letters
    """
    a = introcs.count_str(w,'a')
    e = introcs.count_str(w,'e')
    i = introcs.count_str(w,'i')
    o = introcs.count_str(w,'o')
    u = introcs.count_str(w,'u')
    y = introcs.count_str(w[1:],'y')
    return a+e+i+o+u+y
