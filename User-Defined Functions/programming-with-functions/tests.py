"""
The test script for the course project.

Author: Orlando McEwan
Date: 08/27/2022
"""

import introcs
import funcs

def test_matching_parens():
  """
  Test procedure for matching_parens
  """
  print('Testing matching_parens')
  
  result = funcs.matching_parens('')
  introcs.assert_equals(False, result)
  
  result = funcs.matching_parens('()')
  introcs.assert_equals(True, result)
  
  result = funcs.matching_parens('(Hello')
  introcs.assert_equals(False, result)
  
  result = funcs.matching_parens('Hello)')
  introcs.assert_equals(False, result)
  
  result = funcs.matching_parens('(H(ello))')
  introcs.assert_equals(True, result)
  
  result = funcs.matching_parens('(H)(e)llo')
  introcs.assert_equals(True, result)

  result = funcs.matching_parens('(He(llo)')
  introcs.assert_equals(True, result)
  
  
def test_first_in_parens():
  """
  Test procedure for first_in_parens
  """
  print("Testing first_in_parens")
  
  result = funcs.first_in_parens('h (i) m')
  introcs.assert_equals('i', result)
  
  result = funcs.first_in_parens('h (I) (m)')
  introcs.assert_equals('I', result)
  
  result = funcs.first_in_parens('h ((o) (m)) e')
  introcs.assert_equals('(o', result)
  
  result = funcs.first_in_parens('(home)')
  introcs.assert_equals('home', result)
  
  result = funcs.first_in_parens('()')
  introcs.assert_equals('', result)
  
# Script code
# test_matching_parens()
test_first_in_parens()

print('Module funcs is working correctly')