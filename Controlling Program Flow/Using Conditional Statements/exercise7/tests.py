"""  
A completed test script for the time functions.

Author: Walker M. White
Date: July 30, 2019
"""
import funcs
import introcs


def test_time_to_military():
    """
    Test procedure for the function time_to_military()
    """
    print('Testing time_to_military()')
    
    result = funcs.time_to_military('12:00 AM')
    introcs.assert_equals('00:00',result)
    
    result = funcs.time_to_military('12:00 PM')
    introcs.assert_equals('12:00',result)
    
    result = funcs.time_to_military('9:05 AM')
    introcs.assert_equals('09:05',result)
    
    result = funcs.time_to_military('10:30 AM')
    introcs.assert_equals('10:30',result)
    
    result = funcs.time_to_military('11:15 AM')
    introcs.assert_equals('11:15',result)
    
    result = funcs.time_to_military('9:05 PM')
    introcs.assert_equals('21:05',result)
    
    result = funcs.time_to_military('11:15 PM')
    introcs.assert_equals('23:15',result)
    
    result = funcs.time_to_military('10:30 PM')
    introcs.assert_equals('22:30',result)


def test_time_to_minutes():
    """
    Test procedure for the function time_to_minutes()
    """
    print('Testing time_to_minutes()')
    
    result = funcs.time_to_minutes('9:05 AM')
    introcs.assert_equals(545,result)
    
    result = funcs.time_to_minutes('10:30 AM')
    introcs.assert_equals(630,result)
    
    result = funcs.time_to_minutes('11:15 AM')
    introcs.assert_equals(675,result)
    
    result = funcs.time_to_minutes('12:00 AM')
    introcs.assert_equals(0,result)
    
    result = funcs.time_to_minutes('9:05 PM')
    introcs.assert_equals(1265,result)
    
    result = funcs.time_to_minutes('11:15 PM')
    introcs.assert_equals(1395,result)
    
    result = funcs.time_to_minutes('10:30 PM')
    introcs.assert_equals(1350,result)
    
    result = funcs.time_to_minutes('12:00 PM')
    introcs.assert_equals(720,result)


test_time_to_military()
test_time_to_minutes()
print('Module funcs passed all tests.')