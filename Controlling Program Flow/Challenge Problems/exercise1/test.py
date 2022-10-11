"""
Test script for the findall function

Author: Walker M. White
Date: July 30, 2019
"""
import func
import introcs


def test_findall():
    """
    Tests procedure for function findall().
    """
    print('Testing findall()')
    
    text = 'how now brown cow'
    result = func.findall(text,'ow')
    introcs.assert_equals((1, 5, 10, 15),result)
    
    result = func.findall(text,'brown')
    introcs.assert_equals((8,),result)
    
    result = func.findall(text,'cat')
    introcs.assert_equals((),result)
    
    result = func.findall('jeeepeeer','ee')
    introcs.assert_equals((1, 2, 5, 6),result)
    
    result = func.findall('','a')
    introcs.assert_equals((),result)
    
    result = func.findall('the cat in the hat had a sad','a')
    introcs.assert_equals((5, 16, 20, 23, 26),result)


if __name__ == '__main__':
    test_findall()
    print('Module func passed all tests.')