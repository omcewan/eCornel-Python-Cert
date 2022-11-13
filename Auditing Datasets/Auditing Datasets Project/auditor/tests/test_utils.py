"""
Test procedures for the utility functions for this project.

These tests read and write from files in the same directory as this file.

Author: Walker M. White (wmw2)
Date:   June 7, 2019
"""

import os.path
import json
# See: https://stackoverflow.com/questions/14132789/relative-imports-for-the-billionth-time
if __package__ is None or __package__ == '':
    # Access the module if run from __main__.py (Script visibility)
    from support import *
else:
    # Access the module if run from __init__.py (Packages visibility)
    from .support import *


# Load the utils modle
utils = load_from_path('utils')


# DATA TO TEST AGAINST
# The proper contents for file1.csv
FILE1 = [['STUDENT','AIRPLANE','INSTRUCTOR','TAKEOFF','LANDING','FILED','AREA'],
['S00309','738GG','I076','2015-01-12T09:00:00-05:00','2015-01-12T11:00:00-05:00','VFR','Pattern'],
['S00308','133CZ','I053','2015-01-13T09:00:00-05:00','2015-01-13T12:00:00-05:00','VFR','Practice Area'],
['S00324','426JQ','I053','2015-02-04T11:00:00-05:00','2015-02-04T14:00:00-05:00','VFR','Cross Country'],
['S00319','811AX','I072','2015-02-06T13:00:00-05:00','2015-02-06T15:00:00-05:00','VFR','Pattern'],
['S00321','738GG','I072','2015-02-08T10:00:00-05:00','2015-02-08T13:00:00-05:00','VFR','Practice Area'],
['S00308','811AX','I072','2015-02-23T09:00:00-05:00','2015-02-23T13:00:00-05:00','VFR','Cross Country']]


# The proper contents for file2.csv
FILE2 = [['TAIL NO','TYPE','CAPABILITY','ADVANCED','MULTIENGINE','ANNUAL','HOURS'],
['133CZ','Cessna 152','VFR','No','No','2016-04-15','88'],
['811AX','Cessna 152','VFR','No','No','2016-01-22','39'],
['426JQ','Cessna 152','VFR','No','No','2016-07-30','31']]


# The proper contents for file3.json
FILE3 = {
    "2018-01-01T00:00:00-05:00": {
        "visibility": {
            "prevailing": 1.75,
            "units": "SM"
        },
        "wind": {
            "speed": 13.0,
            "crosswind": 5.0,
            "units": "KT"
        },
        "temperature": {
            "value": -15.0,
            "units": "C"
        },
        "sky": [
            {
                "cover": "clouds",
                "type": "broken",
                "height": 1200.0,
                "units": "FT"
            },
            {
                "type": "overcast",
                "height": 1800.0,
                "units": "FT"
            }
        ],
        "weather": [
            "light snow",
            "mist"
        ],
        "code": "201801010456Z"
    },
    "2017-12-31T23:00:00-05:00": {
        "visibility": {
            "prevailing": 1.75,
            "units": "SM"
        },
        "wind": {
            "speed": 13.0,
            "crosswind": 5.0,
            "units": "KT"
        },
        "temperature": {
            "value": -15.0,
            "units": "C"
        },
        "sky": [
            {
                "cover": "clouds",
                "type": "broken",
                "height": 1300.0,
                "units": "FT"
            },
            {
                "type": "overcast",
                "height": 2200.0,
                "units": "FT"
            }
        ],
        "weather": [
            "light snow",
            "mist"
        ],
        "code": "201801010356Z"
    },
    "2017-12-31T22:00:00-05:00": {
        "visibility": {
            "prevailing": 3.0,
            "units": "SM"
        },
        "wind": {
            "speed": 11.0,
            "crosswind": 7.0,
            "units": "KT"
        },
        "temperature": {
            "value": -15.0,
            "units": "C"
        },
        "sky": [
            {
                "type": "overcast",
                "height": 1300.0,
                "units": "FT"
            }
        ],
        "weather": [
            "light snow",
            "mist"
        ],
        "code": "201801010317Z"
    },
    "2017-12-31T21:00:00-05:00": {
        "visibility": {
            "prevailing": 10.0,
            "units": "SM"
        },
        "wind": {
            "speed": 10.0,
            "crosswind": 7.0,
            "units": "KT"
        },
        "temperature": {
            "value": -16.1,
            "units": "C"
        },
        "sky": [
            {
                "type": "overcast",
                "height": 1700.0,
                "units": "FT"
            }
        ],
        "code": "201801010156Z"
    }
}


# TEST FUNCTIONS
def test_read_csv():
    """
    Tests the function utils.read_csv
    """
    fcn = 'utils.read_csv'
    
    # Access the file relative to this one, not the user's terminal
    parent = os.path.split(__file__)[0]
    fpath  = os.path.join(parent,'file1.csv')
    table = utils.read_csv(fpath)
    
    assert_equals(list, type(table),
                  '%s did not return a list: %s' % (fcn,repr(table)))
    assert_true(len(table) > 0 and type(table[0]) == list,
                  '%s did not return a nested list: %s' % (fcn,repr(table)))
    assert_true(len(table[0]) > 0 and type(table[0][0]) == str,
                  '%s did not return a 2d list of strings: %s' % (fcn,repr(table)))
    assert_equals(FILE1, table,
                  '%s did not return the correct 2d list: %s vs %s' % (fcn,repr(table), repr(FILE1)))
    
    print('  %s passed all tests' % fcn)


def test_write_csv():
    """
    Tests the function utils.write_csv
    """
    fcn = 'utils.write_csv'
    
    # Make the file in this directory
    parent = os.path.split(__file__)[0]
    fpath  = os.path.join(parent,'file2.csv')
    utils.write_csv(FILE2,fpath)
    
    assert_true(os.path.isfile(fpath),'%s did not create a file' % fcn)
    
    file = open(fpath)
    data = file.read()
    file.close()
    assert_true(len(data) > 0,'%s did not write anything to the file' % fcn)
    
    data = data.strip().split('\n')
    assert_equals(len(FILE2), len(data),
                  '%s did not write the correct number of lines' % fcn)
    
    # And check each line
    for pos in range(len(data)):
        line = data[pos].strip().split(',')
        assert_equals(FILE2[pos], line,
                      '%s did not write the correct values for line %d' % (fcn,pos))
    
    print('  %s passed all tests' % fcn)


def test_read_json():
    """
    Tests the function utils.read_json
    """
    fcn = 'utils.read_json'
    
    # Access the file relative to this one, not the user's terminal
    parent = os.path.split(__file__)[0]
    fpath = os.path.join(parent,'file3.json')
    data  = utils.read_json(fpath)
    
    assert_equals(dict, type(data),
                  '%s did not return the correct type: %s' % (fcn,repr(data)))
    assert_equals(FILE3, data,
                  '%s did not return the correct dictionary: %s vs %s' % (fcn,repr(data), repr(FILE3)))
    
    fpath = os.path.join(parent,'file4.json')
    data  = utils.read_json(fpath)
    assert_equals(list, type(data),
                  '%s did not return the correct type: %s' % (fcn,repr(data)))
    thelist = FILE3['2018-01-01T00:00:00-05:00']['sky']
    assert_equals(thelist, data,
                  '%s did not return the correct list: %s vs %s' % (fcn,repr(data), repr(thelist)))
    
    print('  %s passed all tests' % fcn)


def test_str_to_time():
    """
    Tests the function utils.str_to_time
    """
    fcn = 'utils.str_to_time'
    
    from dateutil.parser import parse
    from pytz import timezone
    
    input   = '2016-05-12'
    assert_equals(parse(input), utils.str_to_time(input),
                  '%s did not properly parse %s' % (fcn,repr(input)))
    
    input   = '16:23'
    assert_equals(parse(input), utils.str_to_time(input),
                  '%s did not properly parse %s' % (fcn,repr(input)))
    
    input   = '16:23-4:00'
    assert_equals(parse(input), utils.str_to_time(input),
                  '%s did not properly parse %s' % (fcn,repr(input)))
    
    input   = '2016-05-12T16:23-4:00'
    assert_equals(parse(input), utils.str_to_time(input),
                  '%s did not properly parse %s' % (fcn,repr(input)))
    
    input   = '2016-05-12T16:23'
    correct = parse(input+'-4:00')
    assert_equals(correct, utils.str_to_time(input,correct),
                  '%s did not properly assign time zone %s' % (fcn,repr(correct.tzinfo)))
    
    input   = '2016-05-12T16:23'
    correct = parse(input+'-5:00')
    offset =  parse(input+'-4:00')
    result  = utils.str_to_time(input+'-5:00',offset)
    assert_equals(correct, result,
                  '%s overwrote a previously existing time zone: %s vs %s' % (fcn,repr(result.tzinfo),repr(correct.tzinfo)))
    
    input   = '2016-05-12T16:23'
    central = 'America/Chicago'
    correct = timezone(central).localize(parse(input))
    result  =  utils.str_to_time(input,central)
    assert_equals(correct, result, '%s could not handle time zone string %s' % (fcn,repr(central)))
    
    print('  %s passed all tests' % fcn)

def test_daytime():
    """
    Tests the function utils.daytime
    """
    fcn = 'utils.daytime'
    
    parent = os.path.split(__file__)[0]
    fpath  = os.path.join(parent,'daycycle.json')
    cycle = utils.read_json(fpath)
    
    times = [('2015-06-05T07:00:00',True,True),  ('2015-06-05T17:00:00',True,True),
             ('2015-10-31T06:00:00',False,True), ('2015-10-31T17:00:00',True,False),
             ('2015-11-17T07:00:00',True,True),  ('2015-11-17T17:00:00',False,False),
             ('2015-12-11T07:00:00',False,True), ('2015-06-05T17:00:00',True,True),
             ('2016-11-01T07:00:00',True,True),  ('2016-11-01T17:00:00',False,False),
             ('2017-11-17T07:00:00',False,True), ('2017-11-17T17:00:00',False,False),
             ('2018-06-05T07:00:00',True,True),  ('2018-06-05T17:00:00',True,True),
             ('2018-11-15T07:00:00',True,True),  ('2018-11-15T17:00:00',False,False),
             ('2019-11-15T07:00:00',True,True),  ('2019-11-15T17:00:00',False,False)]
    
    # CHECK THE TEST CASES
    for time in times:
        act  = utils.str_to_time(time[0],"America/New_York")
        day  = utils.daytime(act,cycle)
        data = (fcn,repr(act),'daycycle',repr(day),repr(time[1]))
        assert_equals(time[1], day,'%s(%s,%s) returned %s, but should have returned %s' % data)
        
        act  = utils.str_to_time(time[0],"America/Chicago")
        day  = utils.daytime(act,cycle)
        data = (fcn,repr(act),'daycycle',repr(day),repr(time[2]))
        assert_equals(time[2], day,'%s(%s,%s) returned %s, but should have returned %s' % data)

        # Test the case of no time zone (Same result as first test above) (Edited by STT)
        act  = utils.str_to_time(time[0])
        day  = utils.daytime(act,cycle)
        data = (fcn,repr(act),'daycycle',repr(day),repr(time[1]))
        assert_equals(time[1], day,'%s(%s,%s) returned %s, but should have returned %s' % data)
    
    print('  %s passed all tests' % fcn)


def test_get_for_id():
    """
    Tests the function utils.get_for_id
    """
    fcn = 'utils.get_for_id'
    
    # With header
    result = utils.get_for_id('S00324',FILE1)
    assert_equals(FILE1[3], result,
                  '%s was unable to find student %s in %s' % (fcn,repr('S00324'),repr(FILE1)))
    
    # Without header
    result = utils.get_for_id('S00324',FILE1[1:])
    assert_equals(FILE1[3], result,
                  '%s was unable to find student %s in %s' % (fcn,repr('S00324'),repr(FILE1[1:])))
    
    # Next table
    result = utils.get_for_id('811AX',FILE2)
    assert_equals(FILE2[2], result,
                  '%s was unable to find plane %s in %s' % (fcn,repr('811AX'),repr(FILE2)))
    
    # Bad query
    result = utils.get_for_id('XXXXXX',FILE1)
    assert_equals(None, result, '%s could not properly handle a missing id'% fcn)
    
    print('  %s passed all tests' % fcn)


def test():
    """
    Performs all tests on the module utils.
    """
    print('Testing module utils')
    test_read_csv()
    test_write_csv()
    test_read_json()
    test_str_to_time()
    test_daytime()
    test_get_for_id()
