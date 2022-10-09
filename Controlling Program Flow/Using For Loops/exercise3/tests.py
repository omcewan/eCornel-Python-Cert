"""
Test script for the for-loop functions

Author: Walker M. White
Date: July 30, 2019
"""
import introcs
import funcs


def test_factorial():
    """
    Test procedure for function factorial().
    """
    print('Testing factorial()')
    
    result = funcs.factorial(0)
    introcs.assert_equals(1,result)
    
    result = funcs.factorial(1)
    introcs.assert_equals(1,result)
    
    result = funcs.factorial(2)
    introcs.assert_equals(2,result)
    
    result = funcs.factorial(3)
    introcs.assert_equals(6,result)
    
    result = funcs.factorial(5)
    introcs.assert_equals(120,result)
    
    result = funcs.factorial(8)
    introcs.assert_equals(40320,result)


def test_revrange():
    """
    Test procedure for function revrange().
    """
    print('Testing revrange()')
    
    result = funcs.revrange(0,3)
    introcs.assert_equals((2,1,0),result)
    
    result = funcs.revrange(0,4)
    introcs.assert_equals((3,2,1,0),result)
    
    result = funcs.revrange(5,10)
    introcs.assert_equals((9,8,7,6,5),result)
    
    result = funcs.revrange(3,3)
    introcs.assert_equals((),result)


if __name__ == '__main__':
    test_factorial()
    test_revrange()
    print('Module funcs passed all tests.')