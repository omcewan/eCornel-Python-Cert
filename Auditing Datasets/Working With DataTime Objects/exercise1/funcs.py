"""
Functions for working with datetime objects.

Author: Orlando McEwan
Date:   11/06/2022
"""
import datetime


def christmas_day(year):
    """
    Returns ISO day of the week for Christmas in the given year.

    The ISO day is an integer between 1 and 7.  It is 1 for Monday, 7 for Sunday 
    and the appropriate number for any day in-between. 

    Parameter year: The year to check for Christmas
    Precondition: years is an int > 0 (and a year using the Gregorian calendar)
    """
    # HINT: Make a date object and use the isoweekday method

    date = datetime.date(year, 12, 25)

    xmas_day = date.isoweekday()

    return xmas_day


def iso_str(d, t):
    """
    Returns the ISO formatted string of date and time together.

    When combining, the time must be accurate to the microsecond.

    Parameter d: The month-day-year
    Precondition: d is a date object

    Parameter t: The time of day
    Precondition: t is a time object
    """
    # HINT: Combine date and time into a datetime and use isoformat

    date_time = datetime.datetime(
        d.year, d.month, d.day, t.hour, t.minute, t.second, t.microsecond)

    return date_time.isoformat()
