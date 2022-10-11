"""
Test script for the encode function

Author: Walker M. White
Date: July 30, 2019
"""
import introcs
import func


def test_encode():
    """
    Tests procedure for function encode().
    """
    print('Testing encode()')
    
    # Start with the original Caesar example
    result = func.encode('attackatdawn',3)
    introcs.assert_equals('dwwdfndwgdzq',result)
    
    # Decode with 26-3
    result = func.encode(result,23)
    introcs.assert_equals('attackatdawn',result)
    
    # Rot 13
    result = func.encode('attackatdawn',13) 
    introcs.assert_equals('nggnpxngqnja',result)
    
    result = func.encode(result,13)
    introcs.assert_equals('attackatdawn',result)
    
    result = func.encode('ordertheretreat',13)
    introcs.assert_equals('beqregurergerng',result)
    
    result = func.encode(result,13)
    introcs.assert_equals('ordertheretreat',result)
    
    # Once more test
    result = func.encode('letsmeetforlunch',10)
    introcs.assert_equals('vodcwoodpybvexmr',result)
    
    result = func.encode(result,16)
    introcs.assert_equals('letsmeetforlunch',result)
    
    # Empty string
    result = func.encode('',25)
    introcs.assert_equals('',result)



if __name__ == '__main__':
    test_encode()
    print('Module func passed all tests.')