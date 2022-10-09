"""
A test script for the function eval_frac.

This test script shows how to provide proper code coverage for a function with
try-except in it.

Author: Walker M. White
Date:   March 30, 2019
"""
import introcs              # testing functions
import frac                 # function to be tested


def test_eval_frac():
    """
    Test procedure for the function eval_frac
    """
    print('Testing eval_frac')
    # Start with a good test
    result = frac.eval_frac('2/10')
    introcs.assert_floats_equal(0.2, result)
    
    # Now a lot of error tests
    
    # Slash in bad places
    result = frac.eval_frac('12/')
    introcs.assert_equals(None, result)
    
    result = frac.eval_frac('/12')
    introcs.assert_equals(None, result)
    
    # Non numbers around slash
    result = frac.eval_frac('12/a')
    introcs.assert_equals(None, result)
    
    result = frac.eval_frac('a/12')
    introcs.assert_equals(None, result)
    
    # Non-ints around slash
    result = frac.eval_frac('12/13.5')
    introcs.assert_equals(None, result)
    
    result = frac.eval_frac('13.5/12')
    introcs.assert_equals(None, result)
    
    # Division by 0
    result = frac.eval_frac('0/12')
    introcs.assert_floats_equal(0.0, result)
    
    result = frac.eval_frac('12/0')
    introcs.assert_equals(None, result)


# Script code.  This is ignored on input
if __name__ == '__main__':
    test_eval_frac()
    print('Module frac is working correctly')
