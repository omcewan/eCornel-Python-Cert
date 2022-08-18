"""
Unit test for the module vowels

This module demonstrates the most primitive form of testing script.  It performs
the tests directly, without wrapping them in a test procedure.

This gives you an idea of the type of testing you might do with a function.
Believe it or not, this script does not have near enough tests.

Author: Walker M. White
Date:   February 14, 2019
"""
import introcs          # introcs assert functions
import vowels           # function to be tested

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

# We really needed to test more vowel combinations for the "2" case

# Everything is ok
print('Module vowels is working correctly')
