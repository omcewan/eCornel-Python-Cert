"""
Test script for the exponential function

Author: Walker M. White
Date: July 30, 2019
"""
import introcs
import func


def test_exp():
    """
    Tests procedure for function exp().
    """
    print('Testing exp()')
    
    # Note that we round the result to ignore anything outside margin of error
    result = round(func.exp(1),5)
    introcs.assert_floats_equal(2.71828, result)
    
    result = round(func.exp(1,1e-12),11)
    introcs.assert_floats_equal(2.71828182846, result)
    
    result = round(func.exp(-2),5)
    introcs.assert_floats_equal(0.13534, result)
    
    result = round(func.exp(-2,1e-12),11)
    introcs.assert_floats_equal(0.13533528324, result)
    
    result = round(func.exp(8,1e-1),0)
    introcs.assert_floats_equal(2981.0, result)
    
    result = round(func.exp(8),5)
    introcs.assert_floats_equal(2980.95799, result)
    
    result = round(func.exp(8),11)
    introcs.assert_floats_equal(2980.95798664543, result)



if __name__ == '__main__':
    test_exp()
    print('Module func passed all tests.')