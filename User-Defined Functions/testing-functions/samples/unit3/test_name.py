"""
Unit test for the module name

This module demonstrates the most primitive form of testing script.  It performs
the tests directly, without wrapping them in a test procedure.

Author: Walker M. White
Date:   February 14, 2019
"""
import introcs          # introcs assert functions
import name             # function to be tested

# Test case 1
result = name.last_name_first('Walker White')
introcs.assert_equals('White, Walker',result)

# Test case 2
result = name.last_name_first('Walker     White')
introcs.assert_equals('White, Walker',result)

# Everything is ok
print('Module name is working correctly')
