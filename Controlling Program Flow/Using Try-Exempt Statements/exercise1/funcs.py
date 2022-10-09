"""
A module to demonstrate how to test precondition enforcement.

This module has a function (and a helper) that uses assert statements to enforce 
the preconditions.

Author: Orlando McEwan
Date: 10/09/2022
"""
import introcs


def valid_format(s):
    """
    Returns True if s is a string in 12-format <hours>:<min> AM/PM

    Example:
        valid_format('2:45 PM') returns True
        valid_format('2:45PM') returns False
        valid_format('14:45') returns False
        valid_format('14:45 AM') returns False
        valid_format(245) returns False

    Parameter s: the candidate time to format
    Precondition: NONE (s can be any value)
    """
    if type(s) != str:
        return False
    
    colon = introcs.find_str(s,':')
    if colon == -1:
        return False
    elif not introcs.isdigit(s[:colon]) or not introcs.isdigit(s[colon+1:colon+3]):
        return False
    
    hrs  = int(s[:colon])
    mins = int(s[colon+1:colon+3])
    if hrs < 1 or hrs > 12 or mins >= 60:
        return False
    
    return s[colon+3:] == ' AM' or s[colon+3:] == ' PM'


def time_to_minutes(s):
    """
    Returns the number of minutes since midnight

    Examples:
       time_to_minutes('2:45 PM') returns 885
       time_to_minutes('9:05 AM'_ returns 545
       time_to_minutes('12:00 AM') returns 0

    Parameter s: string representation of the time
    Precondition: s is a string in 12-format '<hours>:<min> AM/PM'
    """
    
    assert type(s) == str, 'Parameter s is not a string'
    assert valid_format(s), 'Parameter s is not in correct format'
    # Find the separators
    pos1 = introcs.find_str(s, ':')
    pos2 = introcs.find_str(s, ' ')

    # Get hour and convert to int
    hour = s[:pos1]
    hour = int(hour)

    # Adjust hour to be correct.
    suff = s[pos2+1:]
    if (suff == 'PM'):
        if hour == 12:
            hour = hour
        else:
            hour = hour+12
    elif (suff == 'AM' and hour == 12):
        hour = 0

    # Get min and convert to int
    mins = s[pos1 + 1:pos2]
    mins = int(mins)

    return hour*60+mins



def str_to_minutes(s):
    """
    Returns the number of minutes since midnight.
    
    If s does not represent a time, this function returns -1.
    
    Examples:
       time_to_minutes('2:45 PM') returns 885
       time_to_minutes('9:05 AM') returns 545
       time_to_minutes('12:00 AM') returns 0
       time_to_minutes('12:75 AM') returns -1
       time_to_minutes('apple') returns -1
    
    Parameter s: a string potentially representating a time
    Precondition: s is non-empty
    """
    
    try:
        return time_to_minutes(s)
    except:
        return -1

