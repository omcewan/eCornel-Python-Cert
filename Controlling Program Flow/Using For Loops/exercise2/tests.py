"""
Test script for the for-loop functions

Author: Walker M. White
Date: July 30, 2019
"""
import introcs
import funcs


def test_clamp():
    """
    Test procedure for function clamp().
    """
    print('Testing clamp()')
    
    result = funcs.clamp((-1, 1, 3, 5),0,4)
    introcs.assert_equals((0,1,3,4),result)
    
    result = funcs.clamp((-1, 1, 3, 5),-2,8)
    introcs.assert_equals((-1,1,3,5),result)
    
    result = funcs.clamp((-1, 1, 3, 5),-2,-1)
    introcs.assert_equals((-1,-1,-1,-1),result)
    
    result = funcs.clamp((-1, 1, 3, 5),1,1)
    introcs.assert_equals((1,1,1,1),result)
    
    result = funcs.clamp((1, 3),0,4)
    introcs.assert_equals((1,3),result)
    
    result = funcs.clamp((),0,4)
    introcs.assert_equals((),result)


def test_uniques():
    """
    Test procedure for function uniques().
    """
    print('Testing uniques()')
    
    result = funcs.uniques((5, 9, 5, 7))
    introcs.assert_equals(3,result)
    
    result = funcs.uniques((5, 5, 1, 'a', 5, 'a'))
    introcs.assert_equals(3,result)
    
    result = funcs.uniques((1, 2, 3, 4, 5))
    introcs.assert_equals(5,result)
    
    result = funcs.uniques((1,))
    introcs.assert_equals(1,result)
    
    result = funcs.uniques(())
    introcs.assert_equals(0,result)


if __name__ == '__main__':
    test_clamp()
    test_uniques()
    print('Module funcs passed all tests.')