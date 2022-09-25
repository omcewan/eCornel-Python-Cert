"""  
A completed test script for the Pig Latin module.

Author: Walker M. White
Date:   February 20, 2019
"""
import coder
import introcs


def test_first_vowel():
    """
    Test procedure for the function first_vowel()
    """
    print('Testing first_vowel()')
    # No vowels
    result = coder.first_vowel('grrm')
    introcs.assert_equals(-1,result)
    
    # Letter a
    result = coder.first_vowel('pat')
    introcs.assert_equals(1,result)
    
    # Letter e
    result = coder.first_vowel('step')
    introcs.assert_equals(2,result)
    
    # Letter i
    result = coder.first_vowel('strip')
    introcs.assert_equals(3,result)
    
    # Letter o
    result = coder.first_vowel('stop')
    introcs.assert_equals(2,result)
    
    # Letter u
    result = coder.first_vowel('truck')
    introcs.assert_equals(2,result)
    
    # Letter y, not a vowel
    result = coder.first_vowel('ygglx')
    introcs.assert_equals(-1,result)
    
    # Letter y as vowel
    result = coder.first_vowel('sky')
    introcs.assert_equals(2,result)
    
    # Various multi-vowel combinations
    result = coder.first_vowel('apple')
    introcs.assert_equals(0,result)
    
    result = coder.first_vowel('sleep')
    introcs.assert_equals(2,result)
    
    result = coder.first_vowel('year')
    introcs.assert_equals(1,result)
    
    # Feel free to add more


def test_pigify():
    """
    Test procedure for the function pigify()
    """
    print('Testing pigify()')
    
    # User tests
    result = coder.pigify('ask')
    introcs.assert_equals('askhay',result)
    
    result = coder.pigify('use')
    introcs.assert_equals('usehay',result)
    
    result = coder.pigify('quiet')
    introcs.assert_equals('ietquay',result)
    
    result = coder.pigify('quay')
    introcs.assert_equals('ayquay',result)
    
    result = coder.pigify('tomato')
    introcs.assert_equals('omatotay',result)
    
    result = coder.pigify('school')
    introcs.assert_equals('oolschay',result)
    
    result = coder.pigify('you')
    introcs.assert_equals('ouyay',result)
    
    result = coder.pigify('sky')
    introcs.assert_equals('yskay',result)
    
    result = coder.pigify('ssssh')
    introcs.assert_equals('sssshay',result)
    
    result = coder.pigify('grrr')
    introcs.assert_equals('grrray',result)


test_first_vowel()
test_pigify()
print('Module coder passed all tests.')