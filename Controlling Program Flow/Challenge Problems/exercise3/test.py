"""
Test script for the blackjack scorer

Author: Walker M. White
Date: July 30, 2019
"""
import introcs
import func


def test_bjack():
    """
    Tests procedure for function bjack().
    """
    print('Testing bjack()')
    
    result = func.bjack(())
    introcs.assert_equals(0,result)
    
    # Test the individual cards
    result = func.bjack(('2H',))
    introcs.assert_equals(2,result)
    
    result = func.bjack(('3D',))
    introcs.assert_equals(3,result)
    
    result = func.bjack(('4C',))
    introcs.assert_equals(4,result)
    
    result = func.bjack(('5S',))
    introcs.assert_equals(5,result)
    
    result = func.bjack(('6H',))
    introcs.assert_equals(6,result)
    
    result = func.bjack(('7D',))
    introcs.assert_equals(7,result)
    
    result = func.bjack(('8C',))
    introcs.assert_equals(8,result)
    
    result = func.bjack(('9S',))
    introcs.assert_equals(9,result)
    
    result = func.bjack(('TH',))
    introcs.assert_equals(10,result)
    
    result = func.bjack(('JD',))
    introcs.assert_equals(10,result)
    
    result = func.bjack(('QC',))
    introcs.assert_equals(10,result)
    
    result = func.bjack(('KS',))
    introcs.assert_equals(10,result)
    
    result = func.bjack(('AH',))
    introcs.assert_equals(11,result)
    
    # Now hand combinations
    result = func.bjack(('2C','TH'))
    introcs.assert_equals(12,result)
    
    result = func.bjack(('3H','5C', '7D', '9S'))
    introcs.assert_equals(24,result)
    
    result = func.bjack(('TS','JD'))
    introcs.assert_equals(20,result)
    
    result = func.bjack(('KS','AD'))
    introcs.assert_equals(21,result)
    
    result = func.bjack(('KS','9C','AD'))
    introcs.assert_equals(20,result)
    
    result = func.bjack(('AS','AC','KH'))
    introcs.assert_equals(12,result)
    
    result = func.bjack(('AS','AC','KH','TD'))
    introcs.assert_equals(22,result)
    
    result = func.bjack(('4H','AS','AD','TC','AH','AC', '2S'))
    introcs.assert_equals(20,result)
    
    result = func.bjack(())
    introcs.assert_equals(0,result)


if __name__ == '__main__':
    test_bjack()
    print('Module func passed all tests.')