"""
A test script to test the module funcs.py

Author: Orlando McEwan
Date: 08/19/2022
"""

import introcs      # For assert_equals and assert_true
import funcs        # This is what we are testing

def test_has_a_vowel():
  """
  Test procedure for has_a_vowel
  """
  print('Testing has_a_vowel')
  
  result = funcs.has_a_vowel('aeiou')
  introcs.assert_equals(True, result)

  result = funcs.has_a_vowel('ant')
  introcs.assert_equals(True, result)

  result = funcs.has_a_vowel('net')
  introcs.assert_equals(True, result)

  result = funcs.has_a_vowel('him')
  introcs.assert_equals(True, result)

  result = funcs.has_a_vowel('month')
  introcs.assert_equals(True, result)

  result = funcs.has_a_vowel('nut')
  introcs.assert_equals(True, result)

  result = funcs.has_a_vowel('madam')
  introcs.assert_equals(True, result)

  result = funcs.has_a_vowel('durable')
  introcs.assert_equals(True, result)

  result = funcs.has_a_vowel('hgnt')
  introcs.assert_equals(False, result)

  result = funcs.has_a_vowel('bottle')
  introcs.assert_equals(True, result)

  result = funcs.has_a_vowel('skymage')
  introcs.assert_equals(True, result)

def test_has_y_vowel():
  """
  Test procedure for has_y_vowel
  """
  print('Testing has_y_vowel')
  
  result = funcs.has_y_vowel('yes')
  introcs.assert_equals(False, result)
  
  result = funcs.has_y_vowel('boy')
  introcs.assert_equals(True, result)
  
  result = funcs.has_y_vowel('yayor')
  introcs.assert_equals(True, result)
  
  result = funcs.has_y_vowel('hello')
  introcs.assert_equals(False, result)
  
# Script Code
test_has_a_vowel()
test_has_y_vowel()
print('Module funcs is working correctly')
