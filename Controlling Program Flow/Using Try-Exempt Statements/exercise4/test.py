"""  
A test script for the function iso_8601.

Author: Orlando McEwan
Date: 10/09/2022
"""
import func
import introcs


def test_iso_8601():
    """
    Test procedure for the function iso_8601()
    """
    print('Testing iso_8601()')
    
    # Put your test cases here
    result = func.iso_8601('')
    introcs.assert_equals(False, result)
    
    result = func.iso_8601('12:01:10')
    introcs.assert_equals(True, result)
    
    result = func.iso_8601('12:01:1')
    introcs.assert_equals(False, result)
    
    result = func.iso_8601('120:01:10')
    introcs.assert_equals(False, result)
    
    result = func.iso_8601('002:001:100')
    introcs.assert_equals(False, result)
    
    result = func.iso_8601(':01:1')
    introcs.assert_equals(False, result)
    
    result = func.iso_8601('12::1')
    introcs.assert_equals(False, result)
    
    result = func.iso_8601('12:01:')
    introcs.assert_equals(False, result)
    
    result = func.iso_8601('12:1:1')
    introcs.assert_equals(False, result)
    
    result = func.iso_8601('1:10:01')
    introcs.assert_equals(True, result)


if __name__ == '__main__':
    test_iso_8601()
    print('Module func passed all tests.')