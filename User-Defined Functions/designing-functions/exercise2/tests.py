"""
A test script to verify the function initials.

This script is complete.  You do not need to modify it.

Author: Walker M. White
Date:   July 1, 2019
"""
import introcs      # For assert_equals
import func         # This is what we are testing


def test_initials():
    """
    Test procedure for second_in_list.
    """
    print('Testing initials')
    
    result = func.initials('John Smith') 
    introcs.assert_equals('J. S.',result)
    
    result = func.initials('Walker White') 
    introcs.assert_equals('W. W.',result)
    
    result = func.initials('alan smith') 
    introcs.assert_equals('a. s.',result)

    result = func.initials('Joan vanDeer') 
    introcs.assert_equals('J. v.',result)


# Script Code
# Do not write below this line
test_initials()
print('Module func is working correctly')