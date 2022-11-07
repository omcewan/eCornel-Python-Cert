"""  
A completed test script for the module func

Author: Walker M. White
Date: November 30, 2019
"""
import func
import introcs
import datetime


def test_is_before():
    """
    Test procedure for the function is_before()
    """
    print('Testing is_before()')
    
    # Find the directory with this file in it
    d1 = datetime.date(2019,10,12)
    d2 = datetime.date(2019,10,15)
    d3 = datetime.datetime(2019,10,12,9,45,15)
    d4 = datetime.datetime(2019,10,12,10,15)
    
    result = func.is_before(d1,d2)
    introcs.assert_equals(True,result)
    
    result = func.is_before(d2,d1)
    introcs.assert_equals(False,result)
    
    result = func.is_before(d3,d4)
    introcs.assert_equals(True,result)
    
    result = func.is_before(d4,d3)
    introcs.assert_equals(False,result)
    
    result = func.is_before(d1,d3)
    introcs.assert_equals(True,result)
    
    result = func.is_before(d3,d1)
    introcs.assert_equals(False,result)
    
    result = func.is_before(d3,d3)
    introcs.assert_equals(False,result)
    
    result = func.is_before(d3,d3)
    introcs.assert_equals(False,result)
 

if __name__ == '__main__':
    test_is_before()
    print('Module func passed all tests.')