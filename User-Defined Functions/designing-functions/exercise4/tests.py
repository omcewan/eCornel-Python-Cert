"""
A test script to test the module funcs.py

Note that there are multiple test procedures, and they are called in the order that 
the functions are (or should be) implemented.

Author: Walker M. White
Date: July 1, 2019
"""
import introcs      # For assert_equals and assert_true
import funcs        # This is what we are testing


def test_get_seconds():
    """
    Test procedure for get_seconds
    """
    print('Testing get_seconds')
    
    # Put your tests below this line
    result = funcs.get_seconds('12:35:15')
    introcs.assert_equals(15,result)
    
    result = funcs.get_seconds('03:02:05')
    introcs.assert_equals(5,result)
    
    result = funcs.get_seconds('00:00:00')
    introcs.assert_equals(0,result)
    
    result = funcs.get_seconds('23:59:59')
    introcs.assert_equals(59,result)
    
    result = funcs.get_seconds('12:12:10')
    introcs.assert_equals(10,result)


def test_get_minutes():
    """
    Test procedure for get_minutes
    """
    print('Testing get_minutes')
    
    # Put your tests below this line
    result = funcs.get_minutes('12:35:15')
    introcs.assert_equals(35,result)
    
    result = funcs.get_minutes('03:02:05')
    introcs.assert_equals(2,result)
    
    result = funcs.get_minutes('00:00:00')
    introcs.assert_equals(0,result)
    
    result = funcs.get_minutes('23:59:59')
    introcs.assert_equals(59,result)
    
    result = funcs.get_minutes('12:10:12')
    introcs.assert_equals(10,result)


def test_get_hours():
    """
    Test procedure for get_hours
    """
    print('Testing get_hours')
    
    # Put your tests below this line
    result = funcs.get_hours('12:35:15')
    introcs.assert_equals(12,result)
    
    result = funcs.get_hours('03:02:05')
    introcs.assert_equals(3,result)
    
    result = funcs.get_hours('00:00:00')
    introcs.assert_equals(0,result)
    
    result = funcs.get_hours('23:59:59')
    introcs.assert_equals(23,result)
    
    result = funcs.get_hours('10:12:12')
    introcs.assert_equals(10,result)


def test_str_to_seconds():
    """
    Test procedure for get_hours
    """
    print('Testing str_to_seconds')
    
    # Put your tests below this line
    result = funcs.str_to_seconds('00:00:00')
    introcs.assert_equals(0,result)
    
    result = funcs.str_to_seconds('00:00:59')
    introcs.assert_equals(59,result)
    
    result = funcs.str_to_seconds('00:01:00')
    introcs.assert_equals(60,result)
    
    result = funcs.str_to_seconds('01:00:00')
    introcs.assert_equals(3600,result)
    
    result = funcs.str_to_seconds('01:01:00')
    introcs.assert_equals(3660,result)
    
    result = funcs.str_to_seconds('01:01:01')
    introcs.assert_equals(3661,result)
    
    result = funcs.str_to_seconds('12:35:15')
    introcs.assert_equals(45315,result)
    
    result = funcs.str_to_seconds('03:02:05')
    introcs.assert_equals(10925,result)
        
    result = funcs.str_to_seconds('23:59:59')
    introcs.assert_equals(86399,result)


# Script Code
# Do not write below this line
test_get_seconds()
test_get_minutes()
test_get_hours()
test_str_to_seconds()
print('Module funcs is working correctly')
