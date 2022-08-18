"""
A test script to test the module funcs.py

Author: Orlando McEwan
Date: 08/18/22
"""
import introcs      # For assert_equals
import funcs        # This is what we are testing


# Put your code below this line
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

# Do not write below this line
print('Module funcs is working correctly')
