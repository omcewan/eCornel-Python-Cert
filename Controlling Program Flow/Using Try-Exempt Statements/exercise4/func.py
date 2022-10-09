"""
A function to check if a string is in valid ISO 8601 format.

Author: Walker M. White
Date: July 30, 2019
"""
import introcs


def iso_8601(s):
    """
    Returns True if s is a string in ISO 8601 format, False otherwise
    
    ISO 8601 format the form 'hh:mm:ss' where h, m, and s are digits.  There must be 
    exactly two digits each for minutes and seconds, so they are padded with 0s when 
    necessary. The hours may either be 1 or 2 digits. For
    more information, see
        
        https://en.wikipedia.org/wiki/ISO_8601#Times
    
    This function does not accept time zones, abbreviated formats, or decimals
    
    Parameter time: The string to check
    Precondition: s is a string
    """
    try:
        pos1 = introcs.index_str(s,':')
        pos2 = introcs.index_str(s,':',pos1+1)
        hour = int(s[:pos1])
        mins = int(s[pos1+1:pos2])
        secs = int(s[pos2+1:])
        
        # Check times in range
        correct = hour >= 0 and hour < 24 and mins >= 0 and mins < 60 and secs >= 0 and secs < 60
        # Check digits correct
        correct = correct and pos2 == pos1+3 and len(s) == pos2+3 and pos1 <= 2
        return correct
    except:
        return False
