"""  
A completed test script for the module funcs

Author: Walker M. White
Date: November 30, 2019
"""
import funcs
import introcs
import os.path
import json


def test_str_to_time():
    """
    Test procedure for the function str_to_time()
    """
    print('Testing str_to_time()')
    
    from dateutil.parser import parse
    from pytz import timezone
    
    input  = '2016-05-12'
    result = funcs.str_to_time(input)
    introcs.assert_equals(parse(input),result)
    
    input  = '16:23'
    result = funcs.str_to_time(input)
    introcs.assert_equals(parse(input),result)
    
    input   = '16:23-4:00'
    result = funcs.str_to_time(input)
    introcs.assert_equals(parse(input),result)
    
    input   = '2016-05-12T16:23-4:00'
    result = funcs.str_to_time(input)
    introcs.assert_equals(parse(input),result)
    
    input   = '2016-05-12T16:23'
    correct = parse(input+'-4:00')
    result  = funcs.str_to_time(input,correct)
    introcs.assert_equals(correct,result)
    
    input   = '2016-05-12T16:23'
    correct = parse(input+'-5:00')
    offset  =  parse(input+'-4:00')
    result  = funcs.str_to_time(input+'-5:00',offset)
    introcs.assert_equals(correct, result)
    
    input   = '2016-05-12T16:23'
    central = 'America/Chicago'
    correct = timezone(central).localize(parse(input))
    result  =  funcs.str_to_time(input,central)
    introcs.assert_equals(correct, result)


def test_daytime():
    """
    Test procedure for the function daytime()
    """
    print('Testing daytime()')
    
    # Find the directory with this file in it
    parent = os.path.split(__file__)[0]
    
    filepath = os.path.join(parent,'daycycle.json')
    file = open(filepath)
    daycycle = json.loads(file.read())
    file.close()
    
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
        act  = funcs.str_to_time(time[0],"America/New_York")
        day  = funcs.daytime(act,daycycle)
        introcs.assert_equals(time[1], day)
        
        act  = funcs.str_to_time(time[0],"America/Chicago")
        day  = funcs.daytime(act,daycycle)
        introcs.assert_equals(time[2], day)

        # Test the case of no time zone (Same result as first test above.) (Added by STT)
        act  = funcs.str_to_time(time[0])
        day  = funcs.daytime(act,daycycle)
        introcs.assert_equals(time[1], day)

if __name__ == '__main__':
    test_str_to_time()
    test_daytime()
    print('Module funcs passed all tests.')