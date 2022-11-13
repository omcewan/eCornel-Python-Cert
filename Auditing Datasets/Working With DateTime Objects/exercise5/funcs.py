"""
Functions for parsing time values and determining daylight hours.

Both of these functions will be used in the main project.  You should hold on to them.

Author: Orlando McEwan
Date:   11/09/2022
"""

from dateutil.parser import parse
from pytz import timezone


def str_to_time(timestamp, tzsource=None):
    """
    Returns the datetime object for the given timestamp (or None if timestamp is 
    invalid).

    This function should just use the parse function in dateutil.parser to
    convert the timestamp to a datetime object.  If it is not a valid date (so
    the parser crashes), this function should return None.

    If the timestamp has a time zone, then it should keep that time zone even if
    the value for tzsource is not None.  Otherwise, if timestamp has no time zone 
    and tzsource is not None, then this function will use tzsource to assign 
    a time zone to the new datetime object.

    The value for tzsource can be None, a string, or a datetime object.  If it 
    is a string, it will be the name of a time zone, and it should localize the 
    timestamp.  If it is another datetime, then the datetime object created from 
    timestamp should get the same time zone as tzsource.

    Parameter timestamp: The time stamp to convert
    Precondition: timestamp is a string

    Parameter tzsource: The time zone to use (OPTIONAL)
    Precondition: tzsource is either None, a string naming a valid time zone,
    or a datetime object.
    """
    # HINT: Use the code from the previous exercise and add time zone handling.
    # Use localize if tzsource is a string; otherwise replace the time zone if not None

    try:
        # parse the string to a datetime object if the timestamp string is valid
        date_time = parse(timestamp)
    except:
        return

    # check if the date_time varible doesn't have a tzinfo and tzsource has a value and not equal to zero
    if date_time.tzinfo == None and tzsource != None:
        # if the tzsource is a string we get the timezone and then we localize it to the date_time variable
        if type(tzsource) == str:
            tz = timezone(tzsource)
            date_time = tz.localize(date_time)
            return date_time
        # if the tzsource is not None meaning it is a datetime object we replace its tzinfo
        elif type(tzsource) != None:
            date_time = date_time.replace(tzinfo=tzsource.tzinfo)
            return date_time
    else:
        return date_time


def daytime(time, daycycle):
    """
    Returns True if the time takes place during the day, False otherwise (and 
    returns None if a key does not exist in the dictionary).

    A time is during the day if it is after sunrise but before sunset, as
    indicated by the daycycle dictionary.

    A daycycle dictionary has keys for several years (as strings).  The value for
    each year is also a dictionary, taking strings of the form 'mm-dd'.  The
    value for that key is a THIRD dictionary, with two keys "sunrise" and
    "sunset".  The value for each of those two keys is a string in 24-hour
    time format.

    For example, here is what part of a daycycle dictionary might look like:

        "2015": {
            "01-01": {
                "sunrise": "07:35",
                "sunset":  "16:44"
            },
            "01-02": {
                "sunrise": "07:36",
                "sunset":  "16:45"
            },
            ...
        }

    In addition, the daycycle dictionary has a key 'timezone' that expresses the
    timezone as a string. This function uses that timezone when constructing
    datetime objects using data from the daycycle dictionary.  Also, if the time
    parameter does not have a timezone, we assume that it is in the same timezone 
    as the daycycle dictionary.

    Parameter time: The time to check
    Precondition: time is a datetime object

    Parameter daycycle: The daycycle dictionary
    Precondition: daycycle is a valid daycycle dictionary, as described above
    """
    # HINT: Use the code from the previous exercise to get sunset AND sunrise
    # Add a timezone to time if one is missing (the one from the daycycle)

    # change the date to a iso form datetime object and the timezone from the daycycle if one is missing
    iso_date = str_to_time(str(time.isoformat()), daycycle["timezone"])

    # get the year value as a string
    year = str(iso_date.year)

    # check if the year is in the keys of the daycycle
    if year in daycycle.keys():

        # get the month-day from the iso_date convert to a string and then see if it is within the keys of the daycycle[year]
        month_day = str(iso_date)[5:10]

        if month_day in daycycle[year].keys():
            # get the values from sunrise and sunset as wee will need this for our new datetime
            sunrise = daycycle[year][month_day]["sunrise"]
            sunset = daycycle[year][month_day]["sunset"]

            # turn the sunrise and sunset into datetime objects with matching year and month
            daycycle_sunrise = str_to_time(
                year + '-' + month_day + " " + sunrise, daycycle["timezone"])
            daycycle_sunset = str_to_time(
                year + '-' + month_day + " " + sunset, daycycle["timezone"])

            return iso_date > daycycle_sunrise and iso_date < daycycle_sunset
        else:
            return
    return
