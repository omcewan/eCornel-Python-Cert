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
print('The module name is working correctly')
