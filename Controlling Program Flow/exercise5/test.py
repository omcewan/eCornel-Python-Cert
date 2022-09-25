"""  
A completed test script for the function valid_format.

Author: Walker M. White
Date: July 30, 2019
"""
import func
import introcs


def test_valid_format():
    """
    Test procedure for the function valid_format()
    """
    print('Testing valid_format()')
    
    # Valid, no commas
    result = func.valid_format('0')
    introcs.assert_equals(True,result)
    
    result = func.valid_format('3')
    introcs.assert_equals(True,result)
    
    result = func.valid_format('12')
    introcs.assert_equals(True,result)
    
    result = func.valid_format('999')
    introcs.assert_equals(True,result)
    
    # Valid, comma
    result = func.valid_format('1,234')
    introcs.assert_equals(True,result)
    
    result = func.valid_format('12,345')
    introcs.assert_equals(True,result)
    
    result = func.valid_format('987,561')
    introcs.assert_equals(True,result)
    
    # Invalid, not numerical
    result = func.valid_format('apple')
    introcs.assert_equals(False,result)
    
    result = func.valid_format('12a')
    introcs.assert_equals(False,result)
    
    result = func.valid_format('a,123')
    introcs.assert_equals(False,result)
    
    result = func.valid_format('123,b')
    introcs.assert_equals(False,result)
    
    result = func.valid_format('@1#')
    introcs.assert_equals(False,result)
    
    # Invalid, bad commas
    result = func.valid_format('12345')
    introcs.assert_equals(False,result)
    
    result = func.valid_format('91,2345')
    introcs.assert_equals(False,result)
    
    result = func.valid_format('123,45')
    introcs.assert_equals(False,result)
    
    result = func.valid_format('91234,5')
    introcs.assert_equals(False,result)
    
    result = func.valid_format('12;345')
    introcs.assert_equals(False,result)
    
    result = func.valid_format('912-345')
    introcs.assert_equals(False,result)
    
    # Invalid, leading zeros
    result = func.valid_format('01')
    introcs.assert_equals(False,result)
    
    result = func.valid_format('099')
    introcs.assert_equals(False,result)
    
    result = func.valid_format('0,999')
    introcs.assert_equals(False,result)

    result = func.valid_format('01,999')
    introcs.assert_equals(False,result)
    
    # Feel free to add more


test_valid_format()
print('Module func passed all tests.')