"""  
A completed test script for the time functions.

This test script is more advanced than normal test scripts in that it uses try-except
statements to check that time_to_minutes enforces its preconditions.

Author: Walker M. White
Date: July 30, 2019
"""
import funcs
import introcs


def test_valid_format():
    """
    Test procedure for the function valid_format()
    """
    print('Testing valid_format()')

    result = funcs.valid_format('2:45 AM')
    introcs.assert_equals(True,result)
    
    result = funcs.valid_format('2:45 PM')
    introcs.assert_equals(True,result)
    
    result = funcs.valid_format('12:45 AM')
    introcs.assert_equals(True,result)
    
    result = funcs.valid_format('12:45 PM')
    introcs.assert_equals(True,result)
    
    result = funcs.valid_format('12:75 AM')
    introcs.assert_equals(False,result)
    
    result = funcs.valid_format('2:45PM')
    introcs.assert_equals(False,result)
    
    result = funcs.valid_format('14:45')
    introcs.assert_equals(False,result)
    
    result = funcs.valid_format('14:45 AM')
    introcs.assert_equals(False,result)
    
    result = funcs.valid_format('PM')
    introcs.assert_equals(False,result)
    
    result = funcs.valid_format(True)
    introcs.assert_equals(False,result)
    
    result = funcs.valid_format(245)
    introcs.assert_equals(False,result)


def test_time_to_minutes():
    """
    Test procedure for the function time_to_minutes()
    """
    print('Testing time_to_minutes()')
    
    result = funcs.time_to_minutes('12:00 AM')
    introcs.assert_equals(0,result)
    
    result = funcs.time_to_minutes('12:00 PM')
    introcs.assert_equals(720,result)
    
    result = funcs.time_to_minutes('9:05 AM')
    introcs.assert_equals(545,result)
    
    result = funcs.time_to_minutes('11:15 AM')
    introcs.assert_equals(675,result)
    
    result = funcs.time_to_minutes('9:05 PM')
    introcs.assert_equals(1265,result)
    
    result = funcs.time_to_minutes('11:15 PM')
    introcs.assert_equals(1395,result)


def test_str_to_minutes():
    """
    Test procedure for the function str_to_minutes()
    """
    print('Testing str_to_minutes()')
    
    result = funcs.str_to_minutes('12:00 AM')
    introcs.assert_equals(0,result)
    
    result = funcs.str_to_minutes('12:00 PM')
    introcs.assert_equals(720,result)
    
    result = funcs.str_to_minutes('9:05 AM')
    introcs.assert_equals(545,result)
    
    result = funcs.str_to_minutes('11:15 AM')
    introcs.assert_equals(675,result)
    
    result = funcs.str_to_minutes('9:05 PM')
    introcs.assert_equals(1265,result)
    
    result = funcs.str_to_minutes('11:15 PM')
    introcs.assert_equals(1395,result)
    
    result = funcs.str_to_minutes('12:75 AM')
    introcs.assert_equals(-1,result)
    
    result = funcs.str_to_minutes('2:45PM')
    introcs.assert_equals(-1,result)
    
    result = funcs.str_to_minutes('14:45')
    introcs.assert_equals(-1,result)
    
    result = funcs.str_to_minutes('14:45 AM')
    introcs.assert_equals(-1,result)
    
    result = funcs.str_to_minutes('PM')
    introcs.assert_equals(-1,result)
    
    result = funcs.str_to_minutes(True)
    introcs.assert_equals(-1,result)
    
    result = funcs.str_to_minutes(245)
    introcs.assert_equals(-1,result)


test_valid_format()
test_time_to_minutes()
test_str_to_minutes()
print('Module funcs passed all tests.')