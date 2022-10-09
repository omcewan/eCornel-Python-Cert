"""  
A completed test script for the function first_vowel.

Author: Walker M. White
Date: July 30, 2019
"""
import func
import introcs


def test_first_vowel():
    """
    Test procedure for the function first_vowel()
    """
    print('Testing first_vowel()')
    # No vowels
    result = func.first_vowel('grrm')
    introcs.assert_equals(-1,result)
    
    # Letter a
    result = func.first_vowel('pat')
    introcs.assert_equals(1,result)
    
    # Letter e
    result = func.first_vowel('step')
    introcs.assert_equals(2,result)
    
    # Letter i
    result = func.first_vowel('strip')
    introcs.assert_equals(3,result)
    
    # Letter o
    result = func.first_vowel('stop')
    introcs.assert_equals(2,result)
    
    # Letter u
    result = func.first_vowel('truck')
    introcs.assert_equals(2,result)
    
    # Letter y, not a vowel
    result = func.first_vowel('ygglx')
    introcs.assert_equals(-1,result)
    
    # Letter y as vowel
    result = func.first_vowel('sky')
    introcs.assert_equals(2,result)
    
    # Various multi-vowel combinations
    result = func.first_vowel('apple')
    introcs.assert_equals(0,result)
    
    result = func.first_vowel('sleep')
    introcs.assert_equals(2,result)
    
    result = func.first_vowel('year')
    introcs.assert_equals(1,result)
    
    # Feel free to add more


test_first_vowel()
print('Module func passed all tests.')