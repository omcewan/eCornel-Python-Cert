"""
Partially completed test script for tuple expansion

Author: Orlando McEwan
Date: 10/22/2022
"""
import introcs
import func


def test_avg():
    """
    Test procedure for function avg().
    """
    print('Testing avg()')
    
    result = func.avg()
    introcs.assert_floats_equal(0,result)
    
    result = func.avg(7, 1, 4, 3, 6, 8)
    introcs.assert_floats_equal(4.833333333333333,result)
    
    result = func.avg(-1, 1, 3, 5)
    introcs.assert_floats_equal(2.0,result)
    
    result = func.avg(2.5)
    introcs.assert_floats_equal(2.5,result)
    
    result = func.avg(1.0, 1.0, 1.0)
    introcs.assert_floats_equal(1.0,result)
    
    # Test range(10,20) here
    a = tuple(range(10,20))
    result = func.avg(*a)
    introcs.assert_floats_equal(14.5, result)
    
if __name__ == '__main__':
    test_avg()
    print('Module func passed all tests.')