"""
Module demonstrating how to write functions with objects.

This module contains two versions of the same function.  One version returns a new
value, while other modifies one of the arguments to contain the new value.

Author: Orlando McEwan
Date: 10/15/2022
"""
import clock


def add_time1(time1, time2):
    """
    Returns the sum of time1 and time2 as a new Time object
    
    DO NOT ALTER time1 or time2, even though they are mutable
    
    Examples: 
        The sum of 12hr 13min and 13hr 12min is 25hr 25min 
        The sum of 1hr 59min and 3hr 2min is 5hr 1min 
    
    Parameter time1: the starting time
    Precondition: time1 is a Time object
    
    Parameter time2: the time to add
    Precondition: time2 is a Time object
    """
    # print(time1, time2)
    
    hours_t1 = time1.hours
    hours_t2 = time2.hours
    total_hours = hours_t1 + hours_t2
    # print(hours_t1, hours_t2)
    
    minutes_t1 = time1.minutes
    minutes_t2 = time2.minutes
    total_minutes = minutes_t1 + minutes_t2
    # print(minutes_t1, minutes_t2)
    
    if total_minutes > 59:
        if total_minutes == 60:
            total_hours += 1
            total_minutes = 0
        else:
            total_hours += 1
            total_minutes = total_minutes - 60
            
    # print(clock.Time(total_hours, total_minutes))
    return clock.Time(total_hours, total_minutes)

def add_time2(time1, time2):
    """
    Modifies time1 to be the sum of time1 and time2
    
    DO NOT RETURN a new time object.  Modify the object time1 instead.
    
    Examples: 
        The sum of 12hr 13min and 13hr 12min is 25hr 25min 
        The sum of 1hr 59min and 3hr 2min is 5hr 1min 
    
    Parameter time1: the starting time
    Precondition: time1 is a Time object
    
    Parameter time2: the time to add
    Precondition: time2 is a Time object
    """
    new_time = add_time1(time1, time2)
    time1.hours = new_time.hours
    time1.minutes = new_time.minutes
