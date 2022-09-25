"""
A module to demonstrate debugging with conditionals.

This module contains several functions with bugs in it.  You are to
find and remove the bugs using the techniques introduced in the video.

Author: Walker M. White
Date: July 30, 2019
"""
import introcs


def time_to_military(s):
    """ 
    Returns the time in 24-hour (military) format.
    
    24-hour format has the form '<hours>:<minutes>'. The hours are between 0 and 23, 
    and are always two digits (so there must be a leading zero).  The minutes are 
    between 0 and 59, and are always 2 digits.
    
    Examples:
        time_to_military('2:45 PM') returns '14:45'
        time_to_military('9:05 AM') returns '09:05'
        time_to_military('12:00 AM') returns '00:00'
    
    Parameter s: string representation of the time
    Precondition: s is a string in 12-hour format '<hours>:<min> AM/PM'
    """

    # Split up the string
    pos1 = introcs.find_str(s,':')
    pos2 = introcs.find_str(s,' ')
    
    # Extract hours and minutes
    hour = int(s[:pos1])
    mins = s[pos1+1:pos2]
    suff = s[pos2+1:]
    
    # Adjust hour to be correct.
    if (suff == 'PM'):
        hour += 12
    elif hour == 12:
        hour = 0
    
    # Add a leading zero if necessary
    if (hour <= 10):
        hour = '0'+str(hour)
    else:
        hour = str(hour)
    
    # Glue it back together
    return str(hour)+':'+mins


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
    
    # Find the separators
    pos1 = introcs.find_str(s,':')
    pos2 = introcs.find_str(s,' ')
    
    # Get hour and convert to int
    hour = s[:pos1]
    hour = int(hour)
    
    # Adjust hour to be correct.
    suff = s[pos2+1:]
    if (suff == 'PM'):
        hoar = hour+12
    elif (suff == 'AM' and hour == 12):
        hour = 0
    
    # Get min and convert to int
    mins = s[pos1:pos2]
    mins = int(mins)
    
    return hour*60+mins