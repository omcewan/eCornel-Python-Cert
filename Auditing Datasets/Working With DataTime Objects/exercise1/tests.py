"""  
A completed test script for the module funcs

Author: Walker M. White
Date: November 30, 2019
"""
import funcs
import introcs
import datetime


def test_christmas_day():
    """
    Test procedure for the function christmas_day()
    """
    print('Testing christmas_day()')
    
    day = funcs.christmas_day(2019)
    introcs.assert_equals(3,day)
    
    day = funcs.christmas_day(2018)
    introcs.assert_equals(2,day)
    
    day = funcs.christmas_day(2017)
    introcs.assert_equals(1,day)
    
    day = funcs.christmas_day(2016)
    introcs.assert_equals(7,day)
    
    day = funcs.christmas_day(1984)
    introcs.assert_equals(2,day)
    
    day = funcs.christmas_day(2100)
    introcs.assert_equals(6,day)


def test_iso_str():
    """
    Test procedure for the function iso_str()
    """
    print('Testing iso_str()')
    
    d = datetime.date(2019,10,12)
    
    result = funcs.iso_str(d,datetime.time(12,35,15,205))
    introcs.assert_equals('2019-10-12T12:35:15.000205',result)
    
    result = funcs.iso_str(d,datetime.time(9,15))
    introcs.assert_equals('2019-10-12T09:15:00',result)
    
    result = funcs.iso_str(d,datetime.time(23,59,59))
    introcs.assert_equals('2019-10-12T23:59:59',result)
    
    d = datetime.date(1984,6,5)
    
    result = funcs.iso_str(d,datetime.time(12,35,15,205))
    introcs.assert_equals('1984-06-05T12:35:15.000205',result)
    
    result = funcs.iso_str(d,datetime.time(9,15))
    introcs.assert_equals('1984-06-05T09:15:00',result)
    
    result = funcs.iso_str(d,datetime.time(23,59,59))
    introcs.assert_equals('1984-06-05T23:59:59',result)


if __name__ == '__main__':
    test_christmas_day()
    test_iso_str()
    print('Module funcs passed all tests.')