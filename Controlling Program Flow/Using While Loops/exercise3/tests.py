"""
Test script for the for-loop functions

Author: Walker M. White
Date: July 30, 2019
"""
import introcs
import funcs


def test_skip():
    """
    Test procedure for function skip().
    """
    print('Testing skip()')
    
    
    result = funcs.skip('hello world',1)
    introcs.assert_equals('hello world',result)
    
    result = funcs.skip('hello world',2)
    introcs.assert_equals('hlowrd',result)
    
    result = funcs.skip('hello world',3)
    introcs.assert_equals('hlwl',result)
    
    result = funcs.skip('hello world',4)
    introcs.assert_equals('hor',result)
    
    result = funcs.skip('hello world',5)
    introcs.assert_equals('h d',result)
    
    result = funcs.skip('goodnight moon',4)
    introcs.assert_equals('gnto',result)


def test_fixed_points():
    """
    Test procedure for function fixed_points().
    """
    print('Testing fixed_points()')
    
    result = funcs.fixed_points((0,3,2)) 
    introcs.assert_equals((0,2),result)
    
    result = funcs.fixed_points((0,1,2,3))
    introcs.assert_equals((0,1,2,3),result)
    
    result = funcs.fixed_points((2,1,2,1))
    introcs.assert_equals((1,2),result)
    
    result = funcs.fixed_points((2,2,2,2))
    introcs.assert_equals((2,),result)
    
    result = funcs.fixed_points((3,2,1,0))
    introcs.assert_equals((),result)


if __name__ == '__main__':
    test_skip()
    test_fixed_points()
    print('Module funcs passed all tests.')