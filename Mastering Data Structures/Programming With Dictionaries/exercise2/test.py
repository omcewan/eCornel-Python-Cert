"""
A completed test script for the weather reports

Author: Walker M. White
Date: August 9, 2019
"""
import introcs
import func


def test_reports_above_temp():
    """
    Test procedure for function reports_above_temp().
    """
    print('Testing reports_above_temp()')
    
    weather = introcs.read_json('weather.json')
    
    result = func.reports_above_temp(weather,20)
    introcs.assert_equals(0,result)
    
    result = func.reports_above_temp(weather,10)
    introcs.assert_equals(1,result)
    
    result = func.reports_above_temp(weather,5)
    introcs.assert_equals(58,result)
    
    result = func.reports_above_temp(weather,2)
    introcs.assert_equals(116,result)
    
    result = func.reports_above_temp(weather,0)
    introcs.assert_equals(154,result)
    
    result = func.reports_above_temp(weather,-2)
    introcs.assert_equals(258,result)
    
    result = func.reports_above_temp(weather,-5)
    introcs.assert_equals(392,result)
    
    result = func.reports_above_temp(weather,-10)
    introcs.assert_equals(505,result)
    
    result = func.reports_above_temp(weather,-15)
    introcs.assert_equals(600,result)
    
    result = func.reports_above_temp(weather,-20)
    introcs.assert_equals(646,result)


if __name__ == '__main__':
    test_reports_above_temp()
    print('Module func passed all tests.')