"""  
A completed test script for the module func

Author: Walker M. White
Date: November 30, 2019
"""
import func
import introcs
import datetime


def test_past_a_week():
    """
    Test procedure for the function past_a_week()
    """
    print('Testing past_a_week()')
    
    # Find the directory with this file in it
    d1 = datetime.date(2019,10,12)
    d2 = datetime.date(2019,10,25)
    d3 = datetime.date(2019,10,19)
    d4 = datetime.datetime(2019,10,12,9,45,15)
    d5 = datetime.datetime(2019,10,19,10,15)
    d6 = datetime.datetime(2019,10,19,8,30)
    
    result = func.past_a_week(d1,d2)
    introcs.assert_equals(True,result)
    
    result = func.past_a_week(d2,d1)
    introcs.assert_equals(False,result)
    
    result = func.past_a_week(d1,d3)
    introcs.assert_equals(True,result)
    
    result = func.past_a_week(d2,d3)
    introcs.assert_equals(False,result)
    
    result = func.past_a_week(d1,d5)
    introcs.assert_equals(True,result)
    
    result = func.past_a_week(d4,d5)
    introcs.assert_equals(True,result)
    
    result = func.past_a_week(d4,d6)
    introcs.assert_equals(False,result)
 

if __name__ == '__main__':
    test_past_a_week()
    print('Module func passed all tests.')