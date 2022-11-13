"""
Unit test for the to_celsius function

This is a unit test, but it is not designed as a script.  Instead, it exposes a function
that can be called by the application to do the testing.

Because the application only runs the to_celsius function, this is the only function
tested here.

Author: Walker M. White (wmw2)
Date:   June 7, 2019
"""
import introcs
import temp


def test_to_celsius():
    """
    Tests the function to_celsius
    """
    print('Testing to_celsius.')
    
    result = temp.to_celsius(32.0)
    introcs.assert_floats_equal(0.0,result)
    
    result = temp.to_celsius(212.0)
    introcs.assert_floats_equal(100.0,result)
    
    result = temp.to_celsius(95.0)
    introcs.assert_floats_equal(35.0,result)
    
    print('The function looks correct.')
