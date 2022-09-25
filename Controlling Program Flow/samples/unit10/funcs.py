"""
Functions to anglicize integers in the range 1..999,999

The primary function in this module is anglicize(). This is a
great module to help you understand preconditions.

Author: Walker M. White
Date:   March 30, 2019
"""


def anglicize(n):
    """
    Returns: English equivalent of n.

    Examples:
        3:      "three"
        45:     "forty five"
        100:    "one hundred"
        127:    "one hunded twenty seven"
        1001:   "one thousand one"
        990099: "nine hundred ninety thousand ninety nine

    Parameter: the integer to anglicize
    Precondition: 0 < n < 1,000,000
    """
    if n < 1000:
        return anglicize1000(n)

    # n >= 1000
    # conditional expression to get number 1...999
    if n % 1000 == 0:
        suffix = ''
    else:
        suffix = ' '+anglicize1000(n % 1000)

    return (anglicize1000(n//1000) + ' thousand'+ suffix)


def anglicize1000(n):
    """
    Returns: English equiv of n.

    Parameter: the integer to anglicize
    Precondition: n in 1..999
    """
    if n < 20:
        return anglicize1to19(n)

    # n >= 20
    if n < 100:
        return anglicize20to99(n)

    # n >= 100
    return anglicize100to999(n)


def anglicize1to19(n):
    """
    Returns: English equiv of n.

    Parameter: the integer to anglicize
    Precondition: n in 1..19
    """
    if n == 1:
        return 'one'
    elif n == 2:
        return 'two'
    elif n == 3:
        return 'three'
    elif n == 4:
        return 'four'
    elif n == 5:
        return 'five'
    elif n == 6:
        return 'six'
    elif n == 7:
        return 'seven'
    elif n == 8:
        return 'eight'
    elif n == 9:
        return 'nine'
    elif n == 10:
        return 'ten'
    elif n == 11:
        return 'eleven'
    elif n == 12:
        return 'twelve'
    elif n == 13:
        return 'thirteen'
    elif n == 14:
        return 'fourteen'
    elif n == 15:
        return 'fifteen'
    elif n == 16:
        return 'sixteen'
    elif n == 17:
        return 'seventeen'
    elif n == 18:
        return 'eighteen'

    # n = 19
    return 'nineteen'


def anglicize20to99(n):
    """
    Returns: English equiv of n.

    Parameter: the integer to anglicize
    Precondition: n in 20..99
    """
    return tens(n//10) + ('' if n % 10 == 0 else ' '+anglicize1to19(n % 10))


def anglicize100to999(n):
    """
    Returns: English equiv of n.

    Parameter: the integer to anglicize
    Precondition: n in 100..999
    """
    # Anglicize the first three digits
    hundreds = n % 100
    suffix = ''
    if hundreds > 0 and hundreds < 20:
        suffix = ' '+anglicize1to19(hundreds)
    elif hundreds > 20:
        suffix = ' '+anglicize20to99(hundreds)

    return anglicize1to19(n//100) + ' hundred' + suffix


def tens(n):
    """
    Returns: tens-word for n

    Parameter: the integer to anglicize
    Precondition: n in 2..9
    """
    if n == 2:
        return 'twenty'
    elif n == 3:
        return 'thirty'
    elif n == 4:
        return 'forty'
    elif n == 5:
        return 'fifty'
    elif n == 6:
        return 'sixty'
    elif n == 7:
        return 'seventy'
    elif n == 8:
        return 'eighty'

    return 'ninety'
