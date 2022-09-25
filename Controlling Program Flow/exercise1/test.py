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
    introcs.assert_equals(4,result)
    
    # Letter a
    result = func.first_vowel('pat')
    introcs.assert_equals(1,result)
    
    # Letter e
    result = func.first_vowel('step')
    introcs.assert_equals(2,result)

    # Combinations of a and e
    result = func.first_vowel('beat')
    introcs.assert_equals(1,result)

    result = func.first_vowel('ate')
    introcs.assert_equals(0,result)

    # Letter i
    result = func.first_vowel('strip')
    introcs.assert_equals(3,result)
    
    # Letter o
    result = func.first_vowel('stop')
    introcs.assert_equals(2,result)
    
    # Letter u
    result = func.first_vowel('truck')
    introcs.assert_equals(2,result)
    
    # Various multi-vowel combinations
    result = func.first_vowel('pain')
    introcs.assert_equals(1,result)
    
    result = func.first_vowel('pine')
    introcs.assert_equals(1,result)

    result = func.first_vowel('oil')
    introcs.assert_equals(0,result)

    result = func.first_vowel('use')
    introcs.assert_equals(0,result)

    result = func.first_vowel('sleep')
    introcs.assert_equals(2,result)

    # Technically we should have A LOT more
    # (covering all combinations of pairs)
    # Feel free to add more
    
    # Letter y, not a vowel
    result = func.first_vowel('ygglx')
    introcs.assert_equals(5,result)
    
    # Letter y as vowel
    result = func.first_vowel('sky')
    introcs.assert_equals(2,result)

    # Letter y as both
    result = func.first_vowel('yyng')
    introcs.assert_equals(1,result)

    # Letter y in presence of other vowels
    result = func.first_vowel('year')
    introcs.assert_equals(1,result)

    result = func.first_vowel('bygone')
    introcs.assert_equals(1,result)


# Script code
test_first_vowel()
print('Module func passed all tests.')