"""  
A completed test script for the list functions.

Author: Walker M. White
Date: August 9, 2019
"""
import funcs
import introcs


def test_clamp():
    """
    Test procedure for function clamp().
    """
    print('Testing clamp()')
    
    alist = [-1, 1, 3, 5]
    result = funcs.clamp(alist,0,4)
    introcs.assert_equals(None,result)
    introcs.assert_equals([ 0, 1, 3, 4],alist)
    
    alist = [-1, 1, 3, 5]
    result = funcs.clamp(alist,-2,8)
    introcs.assert_equals(None,result)
    introcs.assert_equals([-1, 1, 3, 5],alist)
    
    alist = [-1, 1, 3, 5]
    result = funcs.clamp(alist,-2,-1)
    introcs.assert_equals(None,result)
    introcs.assert_equals([-1,-1,-1,-1],alist)
    
    alist = [-1, 1, 3, 5]
    result = funcs.clamp(alist,1,1)
    introcs.assert_equals(None,result)
    introcs.assert_equals([ 1, 1, 1, 1],alist)
    
    alist = [-1, 4, -1, 4, 2]
    result = funcs.clamp(alist,0,4)
    introcs.assert_equals(None,result)
    introcs.assert_equals([ 0, 4, 0, 4, 2],alist)
    
    alist = [ 1, 3]
    result = funcs.clamp(alist,0,4)
    introcs.assert_equals(None,result)
    introcs.assert_equals([ 1, 3],alist)
    
    alist = []
    result = funcs.clamp(alist,0,4)
    introcs.assert_equals(None,result)
    introcs.assert_equals([],alist)



def test_removeall():
    """
    Test procedure for removeall
    """
    print('Testing removeall()')
    
    alist = [1,2,2,3,1]
    result = funcs.removeall(alist,1)
    introcs.assert_equals(None,result)
    introcs.assert_equals([2,2,3],alist)
    
    alist = [1,2,2,3,1]
    result = funcs.removeall(alist,2)
    introcs.assert_equals(None,result)
    introcs.assert_equals([1,3,1],alist)
    
    alist = [1,2,2,3,1]
    result = funcs.removeall(alist,5)
    introcs.assert_equals(None,result)
    introcs.assert_equals([1,2,2,3,1],alist)
    
    alist = [3,3,3]
    result = funcs.removeall(alist,3)
    introcs.assert_equals(None,result)
    introcs.assert_equals([],alist)
    
    alist = [3,3,3]
    result = funcs.removeall(alist,1)
    introcs.assert_equals(None,result)
    introcs.assert_equals([3,3,3],alist)
    
    alist = [7]
    result = funcs.removeall(alist,7)
    introcs.assert_equals(None,result)
    introcs.assert_equals([],alist)
    
    alist = []
    result = funcs.removeall(alist,7)
    introcs.assert_equals(None,result)
    introcs.assert_equals([],alist)


# Script code
if __name__ == '__main__':
    test_clamp()
    test_removeall()
    print('Module funcs is working correctly')