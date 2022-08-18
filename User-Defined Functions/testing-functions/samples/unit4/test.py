"""
Unit test for multiple modules

This module illustrates what a proper unit test should look like. Each function being
tested has its own test procedure.

It also has a segment of "script code" that invokes the test procedure when
this module is run as an script.

Author: Walker M. White
Date:   February 14, 2019
"""
import introcs          # introcs assert functions
import name             # function to be tested
import vowels           # another function to be tested


def test_number_vowels():
    """
    Test procedure for number_vowels(w)

    This is only part of the tests that we need for this function.  Ideally, we would
    have even more.
    """
    print('Testing number_vowels')

    # Test case 1
    result = vowels.number_vowels('pat')
    introcs.assert_equals(1,result)

    # Test case 2
    result = vowels.number_vowels('pet')
    introcs.assert_equals(1,result)

    # Test case 3
    result = vowels.number_vowels('pit')
    introcs.assert_equals(1,result)

    # Test case 4
    result = vowels.number_vowels('pot')
    introcs.assert_equals(1,result)

    # Test case 5
    result = vowels.number_vowels('put')
    introcs.assert_equals(1,result)

    # Test case 6
    result = vowels.number_vowels('hate')
    introcs.assert_equals(2,result)

    # Test case 7
    result = vowels.number_vowels('beet')
    introcs.assert_equals(2,result)

    # Test case 8
    result = vowels.number_vowels('sky')
    introcs.assert_equals(1,result)

    # Test case 9
    result = vowels.number_vowels('year')
    introcs.assert_equals(2,result)

    # Test case 10
    result = vowels.number_vowels('xxx')
    introcs.assert_equals(0,result)


def test_last_name_first():
    """
    Test procedure for last_name_first(n)
    """
    print('Testing last_name_first')

    # Test case 1
    result = name.last_name_first('Walker White')
    introcs.assert_equals('White, Walker',result)

    # Test case 2
    result = name.last_name_first('Walker     White')
    introcs.assert_equals('White, Walker',result)


# Script code
test_last_name_first()
test_number_vowels()
print('The modules are working correctly')
