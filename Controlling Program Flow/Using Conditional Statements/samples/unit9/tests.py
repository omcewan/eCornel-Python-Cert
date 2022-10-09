"""
A test script to show off the bugs in bugs.py

Author: Walker M. White
Date:   March 31, 2019
"""
import introcs
from bugs import *      # Change to 'from funcs import *' to test fixed functions


def test_leap_year():
    """
    Test procedure for the function leap_year
    """
    print('Testing leap_year')
    
    result = leap_year(2000)
    introcs.assert_equals(True,result)
    
    result = leap_year(2001)
    introcs.assert_equals(False,result)
    
    result = leap_year(2002)
    introcs.assert_equals(False,result)
    
    result = leap_year(2003)
    introcs.assert_equals(False,result)
    
    result = leap_year(2004)
    introcs.assert_equals(True,result)
    
    result = leap_year(2008)
    introcs.assert_equals(True,result)
    
    result = leap_year(2100)
    introcs.assert_equals(False,result)


def test_days_in_month():
    """
    Test procedure for the function days_in_month
    """
    print('Testing days_in_month')
    
    result = days_in_month(1,2000)
    introcs.assert_equals(31,result)
    
    result = days_in_month(1,2001)
    introcs.assert_equals(31,result)
    
    result = days_in_month(2,2000)
    introcs.assert_equals(29,result)
    
    result = days_in_month(2,2001)
    introcs.assert_equals(28,result)
    
    result = days_in_month(3,2000)
    introcs.assert_equals(31,result)
    
    result = days_in_month(3,2001)
    introcs.assert_equals(31,result)
    
    result = days_in_month(4,2000)
    introcs.assert_equals(30,result)
    
    result = days_in_month(4,2001)
    introcs.assert_equals(30,result)
    
    result = days_in_month(5,2000)
    introcs.assert_equals(31,result)
    
    result = days_in_month(5,2001)
    introcs.assert_equals(31,result)
    
    result = days_in_month(6,2000)
    introcs.assert_equals(30,result)
    
    result = days_in_month(6,2001)
    introcs.assert_equals(30,result)
    
    result = days_in_month(7,2000)
    introcs.assert_equals(31,result)
    
    result = days_in_month(7,2001)
    introcs.assert_equals(31,result)
    
    result = days_in_month(8,2000)
    introcs.assert_equals(31,result)
    
    result = days_in_month(8,2001)
    introcs.assert_equals(31,result)
    
    result = days_in_month(9,2000)
    introcs.assert_equals(30,result)
    
    result = days_in_month(9,2001)
    introcs.assert_equals(30,result)
    
    result = days_in_month(10,2000)
    introcs.assert_equals(31,result)
    
    result = days_in_month(10,2001)
    introcs.assert_equals(31,result)
    
    result = days_in_month(11,2000)
    introcs.assert_equals(30,result)
    
    result = days_in_month(11,2001)
    introcs.assert_equals(30,result)
    
    result = days_in_month(12,2000)
    introcs.assert_equals(31,result)
    
    result = days_in_month(12,2001)
    introcs.assert_equals(31,result)



def test_valid_date():
    """
    Test procedure for the function valid_date
    """
    print('Testing valid_date')
    
    # One-digit month and day
    result = valid_date('2/2/2000')
    introcs.assert_equals(True,result)
    
    # One-digit month, two-digit day
    result = valid_date('1/12/2003')
    introcs.assert_equals(True,result)
    
    # Two-digit month, one-digit day
    result = valid_date('12/1/2003')
    introcs.assert_equals(True,result)
    
    # Two-digit month and day
    result = valid_date('12/12/2003')
    introcs.assert_equals(True,result)
    
    # Zeroed month
    result = valid_date('0/12/2003')
    introcs.assert_equals(False,result)
    
    # Zeroed day
    result = valid_date('12/0/2003')
    introcs.assert_equals(False,result)
    
    # Day 31 in a 30 day month 
    result = valid_date('6/31/2003')
    introcs.assert_equals(False,result)
    
    # Month greater than 12.
    result = valid_date('13/10/2017')
    introcs.assert_equals(False,result)
    
    # February 29th in leap year
    result = valid_date('2/29/2004')
    introcs.assert_equals(True,result)
    
    # February 29th outside leap year
    result = valid_date('2/29/2003')
    introcs.assert_equals(False,result)


# Script code
test_leap_year()
test_days_in_month()
test_valid_date()
print('The module is working correctly')
