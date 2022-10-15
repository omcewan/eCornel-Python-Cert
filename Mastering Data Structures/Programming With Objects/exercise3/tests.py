"""  
A completed test script for the string functions.

Author: Walker M. White
Date: August 9, 2019
"""
import introcs
import funcs


def test_first_in_parens():
    """
    Test procedure for first_in_parens
    """
    print('Testing first_in_parens()')
    
    result = funcs.first_in_parens('A (B) C')
    introcs.assert_equals('B',result)

    result = funcs.first_in_parens('A (B) (C) D')
    introcs.assert_equals('B',result)
    
    result = funcs.first_in_parens('A (B (C) D) E')
    introcs.assert_equals('B (C',result)
    
    result = funcs.first_in_parens('A ) B (C) D')
    introcs.assert_equals('C',result)
    
    result = funcs.first_in_parens('A () D')
    introcs.assert_equals('',result)
    
    result = funcs.first_in_parens('(A D)')
    introcs.assert_equals('A D',result)


def test_isnetid():
    """
    Test procedure for isnetid
    """
    print('Testing isnetid()')
    
    result = funcs.isnetid('wmw2')
    introcs.assert_true(result)
    
    result = funcs.isnetid('jrs1234')
    introcs.assert_true(result)
    
    result = funcs.isnetid('ww9999')
    introcs.assert_true(result)
    
    result = funcs.isnetid('Wmw2')
    introcs.assert_false(result)
    
    result = funcs.isnetid('wMw2')
    introcs.assert_false(result)
    
    result = funcs.isnetid('wmW2')
    introcs.assert_false(result)
    
    result = funcs.isnetid('ww99a99')
    introcs.assert_false(result)
    
    result = funcs.isnetid('#w999')
    introcs.assert_false(result)
    
    result = funcs.isnetid('w#w999')
    introcs.assert_false(result)
    
    result = funcs.isnetid('ww#999')
    introcs.assert_false(result)


# Script code
if __name__ == '__main__':
    test_first_in_parens()
    test_isnetid()
    print('Module funcs is working correctly')