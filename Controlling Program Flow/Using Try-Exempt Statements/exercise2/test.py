"""  
A completed test script for the function iseurofloat.

Author: Walker M. White
Date: July 30, 2019
"""
import func
import introcs


def test_iseurofloat():
    """
    Test procedure for the function iseurofloat()
    """
    print('Testing iseurofloat()')
    
    result = func.iseurofloat('12,5')
    introcs.assert_equals(True,result)
    
    result = func.iseurofloat('12,0')
    introcs.assert_equals(True,result)
    
    result = func.iseurofloat('0,5')
    introcs.assert_equals(True,result)
    
    result = func.iseurofloat('00,5')       # This is consistent with traditional float
    introcs.assert_equals(True,result)

    result = func.iseurofloat('-12,5')
    introcs.assert_equals(True,result)

    result = func.iseurofloat('12')
    introcs.assert_equals(False,result)

    result = func.iseurofloat('12,-5')
    introcs.assert_equals(False,result)

    result = func.iseurofloat(',5')
    introcs.assert_equals(False,result)
    
    result = func.iseurofloat('12,')
    introcs.assert_equals(False,result)
    
    result = func.iseurofloat('apple')
    introcs.assert_equals(False,result)
    
    result = func.iseurofloat('12,5.3')
    introcs.assert_equals(False,result)
    
    result = func.iseurofloat('12.5,3')
    introcs.assert_equals(False,result)
    
    result = func.iseurofloat('12,5,3')
    introcs.assert_equals(False,result)


if __name__ == '__main__':
    test_iseurofloat()
    print('Module func passed all tests.')