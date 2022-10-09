"""  
A completed test script for the function extract_name.

Author: Walker M. White
Date: July 30, 2019
"""
import func
import introcs


def test_extract_name():
    """
    Test procedure for the function extract_name()
    """
    print('Testing extract_name()')
    
    result = func.extract_name('smith.john@megacorp.com')
    introcs.assert_equals('john',result)
    
    result = func.extract_name('WHILOW.BRANDON@megacorp.com')
    introcs.assert_equals('BRANDON',result)
    
    result = func.extract_name('maggie.white@mompop.net')
    introcs.assert_equals('maggie',result)
    
    result = func.extract_name('Bob.Bird@mompop.net')
    introcs.assert_equals('Bob',result)
    
    result = func.extract_name('BB.King@mompop.net')
    introcs.assert_equals('BB',result)
    
    # Feel free to add more


# Script code
test_extract_name()
print('Module func passed all tests.')