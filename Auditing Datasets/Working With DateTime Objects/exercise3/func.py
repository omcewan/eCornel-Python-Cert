"""
A simple function computing time elapsed

Author: Orlando McEwan
Date: 11/07/2022
"""
import datetime


def past_a_week(d1,d2):
    """
    Returns True if event d2 happens at least a week (7 days) after d1.
    
    If d1 is after d2, or d2 is less than a week after d1, this function returns False.
    Values d1 and d2 can EITHER be date objects or datetime objects.  If a date object,
    assume that it happens at midnight of that day. 
    
    Parameter d1: The first event
    Precondition: d1 is EITHER a date object or a datetime object
    
    Parameter d2: The second event
    Precondition: d2 is EITHER a date object or a datetime object
    """
    # HINT: Check the type of d1 or d2. If not a datetime, convert it for comparison
    week = datetime.timedelta(weeks=1)

    if type(d1) == type(d2):
        return d1 < d2 and d2 - d1 >= week
    else:
        if hasattr(d1, "hour"):
            d2_datetime = datetime.datetime(d2.year, d2.month, d2.day, 0, 0, 0)
            return d1 < d2_datetime and d2_datetime - d1 >= week
        else:
            d1_datetime = datetime.datetime(d1.year, d1.month, d1.day, 0, 0, 0)
            return d1_datetime < d2 and d2 - d1_datetime >= week
