"""  
A completed test script for the function replace_first

Author: Walker M. White
Date: August 9, 2019
"""
import introcs
import func


def test_replace_first():
    """
    Test procedure for replace_first
    """
    print('Testing replace_first()')
    
    result = func.replace_first((1,2,3),1,4)
    introcs.assert_equals((4,2,3),result)
    
    result = func.replace_first((1,2,3),2,4)
    introcs.assert_equals((1,4,3),result)
    
    result = func.replace_first((1,2,3),3,4)
    introcs.assert_equals((1,2,4),result)
    
    result = func.replace_first((1,2,3),5,4)
    introcs.assert_equals((1,2,3),result)
    
    result = func.replace_first((1,2,1),1,4)
    introcs.assert_equals((4,2,1),result)
    
    result = func.replace_first((1,2,1,2),2,4)
    introcs.assert_equals((1,4,1,2),result)
    
    result = func.replace_first((2,),2,4)
    introcs.assert_equals((4,),result)
    
    result = func.replace_first((),2,4)
    introcs.assert_equals((),result)


# Script code
if __name__ == '__main__':
    test_replace_first()
    print('Module func is working correctly')