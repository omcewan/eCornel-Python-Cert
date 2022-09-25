"""
A module to demonstrate debugging with if-statements.

This module has several bugs in it, spread across multiple functions.  Read the
specifications carefully for the correct behavior.

Author: Walker M. White
Date:   March 31, 2019
"""
import introcs


def valid_date(date):
    """"
    Returns: True if date is a string representing a valid date.  False otherwise
    
    Examples:
        valid_date('2/29/2004') is True
        valid_date('2/29/2003') is False
    
    Parameter date: The string to check for validity
    Precondition: date is a string in form month/day/year where month is 1 or 2
    digits, day is 1 or 2 digits, and year is 4 digits.
    """
    assert type(date) == str, repr(date)+' is not a string'
    assert introcs.count_str(date,'/')==2, repr(date)+' does not have the right / in it'
    # Will not enforce other preconditions
    
    # Split up string
    pos1 = introcs.find_str(date,'/')
    print('First / at '+str(pos1))      # WATCH
    pos2 = introcs.find_str(date,'/',pos1+3)
    print('Second / at '+str(pos2))     # WATCH
    
    # Turn month, day, and year into ints
    month = int(date[:pos1])
    print('Month is '+str(month))       # WATCH
    day   = int(date[pos1+1:pos2])
    print('Day is '+str(day))           # WATCH
    year = int(date[pos2+1:])
    print('Year is '+str(year))        # WATCH
    
    elif day < 1 or day > days_in_month(month,year):
        print('Day out of range')       # TRACE
        return False
    if month < 1 or month > 12:
        print('MONTH out of range')     # TRACE
        return False
    
    return True


def leap_year(year):
    """
    Returns: True if year is a leap year; otherwise False
    
    Parameter year: The year to check
    Precondition: year is a positive int
    """
    assert type(year) == int, repr(year)+' is not an int'
    assert year > 0, repr(year)+' is not a valid year'
    
    if year % 4 != 0:
        print('Not leap year')      # TRACE
        return False
    elif year % 100 == 0 and year % 400 != 0:
        print('Not leap century')   # TRACE
        return False
    print('Leap year')              # TRACE
    return True


def days_in_month(month,year):
    """
    Returns: The number of days in the given month for the given year

    Examples:
        days_in_month(1,2003) is 31
        days_in_month(2,2003) is 28
        days_in_month(2,2004) is 29.

    Parameter month: The month to check
    Precondition: month is an int 1..12

    Paramter year: The associated year (for leap years)
    Precondition: year is a positive int
    """
    assert type(month) == int, repr(month)+' is not an int'
    assert month >= 1 and month <= 12, repr(month)+' is not a valid month'
    assert type(year) == int, repr(year)+' is not an int'
    assert year > 0, repr(year)+' is not a valid year'
    
    # Unless otherwise specified, we have 31 days
    result = 31
    
    # The 30-day months
    if month == 4 or month == 6 or month == 9 or month == 11:
        print('Month is April, June, September, or November')
        result = 30
    elif leap_year(year):
        print('Month is February')
        result = 29
    
    print('Month '+str(month))
    print(' has '+str(result)+' days') # WATCH
    return result
