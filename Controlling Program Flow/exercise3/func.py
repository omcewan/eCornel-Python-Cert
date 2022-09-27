"""  
A function to extract names from e-mail addresses.

Author: Orlando McEwan
Date: 09/27/2022
"""
import introcs


def extract_name(s):
    """
    Returns the first name of the person in e-mail address s.

    We assume (see the precondition below) that the e-mail address is in one of
    three forms:

        last.first@megacorp.com
        last.first.middle@consultant.biz
        first.last@mompop.net

    where first, last, and middle correspond to the person's first, middle, and
    last name. Names are not empty, and contain only letters. Everything after the 
    @ is guaranteed to be exactly as shown.

    The function preserves the capitalization of the e-mail address.

    Examples: 
        extract_name('smith.john@megacorp.com') returns 'john'
        extract_name('McDougal.Raymond.Clay@consultant.biz') returns 'Raymond'
        extract_name('maggie.white@mompop.net') returns 'maggie'
        extract_name('Bob.Bird@mompop.net') returns 'Bob'

    Parameter s: The e-mail address to extract from
    Precondition: s is in one of the two address formats described above
    """
    # You must use an if-elif-else statement in this function.
    if s[-3:] == 'com':
        return s[introcs.index_str(s, '.') + 1: introcs.index_str(s, '@')]
    elif s[-3:] == 'net':
        return s[:introcs.index_str(s, '.')]
    else:
        first_dot = introcs.index_str(s, '.')
        second_dot = introcs.index_str(s, '.', first_dot + 1,)
        return s[first_dot + 1: second_dot]
