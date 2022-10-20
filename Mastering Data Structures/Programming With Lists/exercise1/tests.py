"""  
A completed test script for the list functions.

Author: Walker M. White
Date: August 9, 2019
"""
import funcs
import introcs


def test_put_in():
    """
    Test procedure for put_in
    """
    print('Testing put_in()')
    
    alist = [0,1,2,4]
    result = funcs.put_in(alist,3)
    introcs.assert_equals(None,result)
    introcs.assert_equals([0,1,2,3,4],alist)
    
    result = funcs.put_in(alist,-1)
    introcs.assert_equals(None,result)
    introcs.assert_equals([-1,0,1,2,3,4],alist)
    
    result = funcs.put_in(alist,2)
    introcs.assert_equals(None,result)
    introcs.assert_equals([-1,0,1,2,2,3,4],alist)
    
    result = funcs.put_in(alist,0)
    introcs.assert_equals(None,result)
    introcs.assert_equals([-1,0,0,1,2,2,3,4],alist)
    
    alist = []
    result = funcs.put_in(alist,0)
    introcs.assert_equals(None,result)
    introcs.assert_equals([0],alist)
    
    result = funcs.put_in(alist,1)
    introcs.assert_equals(None,result)
    introcs.assert_equals([0,1],alist)
    
    alist = ['a','aa','ab','b','ce']
    result = funcs.put_in(alist,'aab')
    introcs.assert_equals(None,result)
    introcs.assert_equals(['a','aa','aab','ab','b','ce'],alist)


def test_rotate():
    """
    Test procedure for rotate
    """
    print('Testing rotate()')
    
    alist = [0,1,3,5]
    result = funcs.rotate(alist)
    introcs.assert_equals(None,result)
    introcs.assert_equals([5,0,1,3],alist)
    
    result = funcs.rotate(alist)
    introcs.assert_equals(None,result)
    introcs.assert_equals([3,5,0,1],alist)
    
    result = funcs.rotate(alist)
    introcs.assert_equals(None,result)
    introcs.assert_equals([1,3,5,0],alist)
    
    result = funcs.rotate(alist)
    introcs.assert_equals(None,result)
    introcs.assert_equals([0,1,3,5],alist)
    
    alist = [9]
    result = funcs.rotate(alist)
    introcs.assert_equals(None,result)
    introcs.assert_equals([9],alist)


# Script code
if __name__ == '__main__':
    test_put_in()
    test_rotate()
    print('Module funcs is working correctly')