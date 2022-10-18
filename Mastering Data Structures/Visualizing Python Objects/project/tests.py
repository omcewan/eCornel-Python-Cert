"""  
A completed test script for the fold functions.

Author: Walker M. White
Date: August 9, 2019
"""
import funcs
import introcs


# Some f values to test
def add(x,y):
    """
    Returns the sum x+y
    
    This works on any types that support addition (numbers, strings, etc.)
    
    Parameter x: The first value to add
    Precondition: x supports addition and x is same type as y
    
    Parameter x: The second value to add
    Precondition: x supports addition and x is same type as y
    """
    return x+y


def sub(x,y):
    """
    Returns the difference x-y
    
    Parameter x: The value to subtract from
    Precondition: x is a number
    
    Parameter y: The value to subtract
    Precondition: y is a number
    """
    return x-y


def remove(s1,s2):
    """
    Returns a copy of s, with all characters in s2 removed.
    
    Examples:
        remove('abc','ab') returns 'c'
        remove('abc','xy') returns 'abc'
        remove('hello world','ol') returns 'he wrd'
    
    Parameter s1: the string to copy
    Precondition: s1 is a string
    
    Parameter s2: the characters to remove
    Precondition: s2 is a string
    """
    result = ''
    for x in s1:
        if not x in s2:
            result = result + x
    return result


# Test test procedures
def test_fold_left():
    """
    Test procedure for fold_left
    """
    print('Testing fold_left()')
    
    # Tuple tests
    result = funcs.fold_left(add,(),3)
    introcs.assert_equals(3,result)
    
    result = funcs.fold_left(sub,(),2)
    introcs.assert_equals(2,result)
    
    result = funcs.fold_left(add,(4,),0)
    introcs.assert_equals(4,result)
    
    result = funcs.fold_left(sub,(4,),0)
    introcs.assert_equals(-4,result)
    
    result = funcs.fold_left(sub,(4,),2)
    introcs.assert_equals(-2,result)
    
    result = funcs.fold_left(add,(1,2,3,4),0)
    introcs.assert_equals(10,result)
    
    result = funcs.fold_left(sub,(1,2,3,4),0)
    introcs.assert_equals(-10,result)
    
    result = funcs.fold_left(sub,(-1,-2,-3,-4),0)
    introcs.assert_equals(10,result)
    
    # String tests
    result = funcs.fold_left(add,'','A')
    introcs.assert_equals('A',result)
    
    result = funcs.fold_left(add,'B','')
    introcs.assert_equals('B',result)
    
    result = funcs.fold_left(add,'bcdefg','a')
    introcs.assert_equals('abcdefg',result)
    
    result = funcs.fold_left(remove,'','a')
    introcs.assert_equals('a',result)
    
    result = funcs.fold_left(remove,'a','a')
    introcs.assert_equals('',result)
    
    result = funcs.fold_left(remove,'b','a')
    introcs.assert_equals('a',result)
    
    result = funcs.fold_left(remove,'abcef','abcefhijklimnop')
    introcs.assert_equals('hijklimnop',result)


def test_fold_right():
    """
    Test procedure for fold_right
    """
    print('Testing fold_right()')
    
    # Tuple tests
    result = funcs.fold_right(add,(),3)
    introcs.assert_equals(3,result)
    
    result = funcs.fold_right(sub,(),2)
    introcs.assert_equals(2,result)
    
    result = funcs.fold_right(add,(4,),0)
    introcs.assert_equals(4,result)
    
    result = funcs.fold_right(sub,(4,),0)
    introcs.assert_equals(4,result)
    
    result = funcs.fold_right(sub,(4,),2)
    introcs.assert_equals(2,result)
    
    result = funcs.fold_right(add,(1,2,3,4),0)
    introcs.assert_equals(10,result)
    
    result = funcs.fold_right(sub,(1,2,3,4),0)
    introcs.assert_equals(-2,result)
    
    result = funcs.fold_right(sub,(1,-2,3,-4),0)
    introcs.assert_equals(10,result)
    
    # String tests
    result = funcs.fold_right(add,'','A')
    introcs.assert_equals('A',result)
    
    result = funcs.fold_right(add,'B','')
    introcs.assert_equals('B',result)
    
    result = funcs.fold_right(add,'bcdefg','a')
    introcs.assert_equals('bcdefga',result)
    
    result = funcs.fold_right(remove,'','a')
    introcs.assert_equals('a',result)
    
    result = funcs.fold_right(remove,'a','a')
    introcs.assert_equals('',result)
    
    result = funcs.fold_right(remove,'b','a')
    introcs.assert_equals('b',result)
    
    # This is counter-intuitive.  Try it out in your head
    result = funcs.fold_right(remove,'abc','d')
    introcs.assert_equals('a',result)
    
    result = funcs.fold_right(remove,'aabc','d')
    introcs.assert_equals('',result)


# Script code
if __name__ == '__main__':
    test_fold_left()
    test_fold_right()
    print('Module funcs is working correctly')