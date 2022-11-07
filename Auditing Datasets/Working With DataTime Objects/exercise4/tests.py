"""  
A completed test script for the module funcs

Author: Walker M. White
Date: November 30, 2019
"""
import funcs
import introcs
import datetime
import os.path
import json


def test_str_to_time():
    """
    Test procedure for the function str_to_time()
    """
    print('Testing str_to_time()')
    
    d = datetime.datetime(2016,4,15)
    result = funcs.str_to_time('2016-04-15')
    introcs.assert_equals(datetime.datetime,type(result))
    introcs.assert_equals(d,result)
    
    d = datetime.datetime(2019,10,12)
    result = funcs.str_to_time('October 12, 2019')
    introcs.assert_equals(datetime.datetime,type(result))
    introcs.assert_equals(d,result)
    
    result = funcs.str_to_time('Octover 12, 2019')
    introcs.assert_equals(None,result)
    
    d = datetime.datetime(2016,4,15,10,15,45)
    result = funcs.str_to_time('2016-04-15T10:15:45')
    introcs.assert_equals(datetime.datetime,type(result))
    introcs.assert_equals(d,result)
    
    d = datetime.datetime(2017,8,2,13,0,15)
    result = funcs.str_to_time('2017-08-02 13:00:15')
    introcs.assert_equals(datetime.datetime,type(result))
    introcs.assert_equals(d,result)
    
    d = datetime.datetime(2019,10,12,22,15)
    result = funcs.str_to_time('10:15 pm, October 12, 2019')
    introcs.assert_equals(datetime.datetime,type(result))
    introcs.assert_equals(d,result)
    
    d = datetime.datetime(2019,10,12,22,15)
    result = funcs.str_to_time('22:15 pm, October 12, 2019')
    introcs.assert_equals(None,result)


def test_sunset():
    """
    Test procedure for the function sunset()
    """
    print('Testing sunset()')
    
    # Find the directory with this file in it
    parent = os.path.split(__file__)[0]
    
    filepath = os.path.join(parent,'daycycle.json')
    file = open(filepath)
    daycycle = json.loads(file.read())
    file.close()
    
    # TEST 1
    d = datetime.date(2017,8,2)
    e = datetime.datetime(2017,8,2,19,24)
    result = funcs.sunset(d,daycycle)
    introcs.assert_equals(datetime.datetime,type(result))
    introcs.assert_equals(e,result)
    
    # TEST 2
    d = datetime.date(2019,12,25)
    e = datetime.datetime(2019,12,25,16,38)
    result = funcs.sunset(d,daycycle)
    introcs.assert_equals(datetime.datetime,type(result))
    introcs.assert_equals(e,result)
    
    # TEST 3
    d = datetime.date(2016,6,2)
    e = datetime.datetime(2016,6,2,19,38)
    result = funcs.sunset(d,daycycle)
    introcs.assert_equals(datetime.datetime,type(result))
    introcs.assert_equals(e,result)
    
    # TEST 3
    d = datetime.date(2016,12,25)
    e = datetime.datetime(2016,12,25,16,39)
    result = funcs.sunset(d,daycycle)
    introcs.assert_equals(datetime.datetime,type(result))
    introcs.assert_equals(e,result)
    
    # TEST 5
    d = datetime.date(2014,6,2)
    result = funcs.sunset(d,daycycle)
    introcs.assert_equals(None,result)
    
    # TEST 6
    d = datetime.date(2022,12,25)
    result = funcs.sunset(d,daycycle)
    introcs.assert_equals(None,result)


if __name__ == '__main__':
    test_str_to_time()
    test_sunset()
    print('Module funcs passed all tests.')