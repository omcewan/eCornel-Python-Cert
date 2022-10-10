"""  
A completed test script for the while-loop functions.

Author: Walker M. White
Date: July 30, 2019
"""
import funcs
import introcs
import random


def test_flips():
    """
    Test procedure for the function flips()
    """
    print('Testing flips()')
    
    # This allows us to "derandomize" random for testing
    # See https://www.statisticshowto.datasciencecentral.com/random-seed-definition/
    random.seed(20)
    
    result = funcs.flips()
    introcs.assert_equals(1,result)
    
    result = funcs.flips()
    introcs.assert_equals(1,result)
    
    result = funcs.flips()
    introcs.assert_equals(2,result)
    
    result = funcs.flips()
    introcs.assert_equals(0,result)
    
    result = funcs.flips()
    introcs.assert_equals(3,result)
    
    result = funcs.flips()
    introcs.assert_equals(0,result)
    
    result = funcs.flips()
    introcs.assert_equals(0,result)


def test_partition():
    """
    Test procedure for the function partition()
    """
    print('Testing partition()')
    
    result = funcs.partition('hello')
    introcs.assert_equals(('eo','hll'),result)
    
    result = funcs.partition('superstar')
    introcs.assert_equals(('uea','sprstr'),result)
    
    result = funcs.partition('scary')
    introcs.assert_equals(('a','scry'),result)
    
    result = funcs.partition('grxlpk')
    introcs.assert_equals(('','grxlpk'),result)
    
    result = funcs.partition('aeiou')
    introcs.assert_equals(('aeiou',''),result)


# Uncomment these test procedures when ready
if __name__ == '__main__':
    #test_flips()
    #test_partition()
    print('Module funcs passed all tests.')