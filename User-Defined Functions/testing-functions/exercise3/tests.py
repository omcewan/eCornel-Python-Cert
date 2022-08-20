"""
A test script to test the module func.py

Author: Orlando McEwan
Date: 08/19/2022
"""
import introcs      # For assert_equals and assert_true
import funcs        # This is what we are testing


def test_replace_first():
    """
    Test procedure for replace_first
    """
    print('Testing replace_first')
    
    # Put your tests below this line
    result = funcs.replace_first('crane', 'a', 'o')
    introcs.assert_equals('crone', result)

    result = funcs.replace_first('poll', 'l', 'o')
    introcs.assert_equals('pool', result)

    result = funcs.replace_first('crane', 'cr', 'b')
    introcs.assert_equals('bane', result)
    
    result = funcs.replace_first('orlando', 'r', 'x')
    introcs.assert_equals('oxlando', result)
    
    result = funcs.replace_first('orlando', 'o', 'x')
    introcs.assert_equals('xrlando', result)
    
    result = funcs.replace_first('orlando', 'r', 'xx')
    introcs.assert_equals('oxxlando', result)
    
    result = funcs.replace_first('orlando', 'or', 'xx')
    introcs.assert_equals('xxlando', result)
    
    result = funcs.replace_first('orlando', 'or', 'x')
    introcs.assert_equals('xlando', result)


# Script Code
# Do not write below this line
test_replace_first()
print('Module funcs is working correctly')
