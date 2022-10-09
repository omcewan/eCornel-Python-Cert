"""
Test script for the for-loop functions

Author: Walker M. White
Date: July 30, 2019
"""
import introcs
import funcs


def test_lesser():
    """
    Test procedure for function lesser().
    """
    print('Testing lesser()')
    tup = (5, 9, 5, 7, 3, 10, 4)
    
    result = funcs.lesser(tup,5)
    introcs.assert_equals(2,result)
    
    result = funcs.lesser(tup,4)
    introcs.assert_equals(1,result)
    
    result = funcs.lesser(tup,3)
    introcs.assert_equals(0,result)
    
    result = funcs.lesser(tup,6)
    introcs.assert_equals(4,result)
    
    result = funcs.lesser(tup,10)
    introcs.assert_equals(6,result)
    
    result = funcs.lesser(tup,20)
    introcs.assert_equals(7,result)


def test_avg():
    """
    Test procedure for function avg().
    """
    print('Testing avg()')
    
    result = funcs.avg( () )
    introcs.assert_floats_equal(0,result)
    
    result = funcs.avg( (7, 1, 4, 3, 6, 8) )
    introcs.assert_floats_equal(4.833333333333333,result)
    
    result = funcs.avg( (-1, 1, 3, 5) )
    introcs.assert_floats_equal(2.0,result)
    
    result = funcs.avg( (2.5,) )
    introcs.assert_floats_equal(2.5,result)
    
    result = funcs.avg( (1.0, 1.0, 1.0) )
    introcs.assert_floats_equal(1.0,result)
    
    tup = tuple(range(10,20))
    result = funcs.avg(tup)
    introcs.assert_floats_equal(14.5,result)


if __name__ == '__main__':
    test_lesser()
    test_avg()
    print('Module funcs passed all tests.')