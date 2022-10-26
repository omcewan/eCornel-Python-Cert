"""  
A completed test script for the nested list functions.

Author: Walker M. White
Date: August 9, 2019
"""
import funcs
import introcs
import copy


def test_crossout():
    """
    Test procedure for function crossout().
    
    Note the use of assert_float_lists_equal for testing (nested) lists
    of floats.
    """
    print('Testing crossout()')
    
    table = [[0.1,0.3,0.5],[0.6,0.2,0.7],[1.5,2.3,0.4]]
    result = funcs.crossout(table,1,2)
    introcs.assert_equals(None,result)
    introcs.assert_float_lists_equal([[0.1,0.3],[1.5,2.3]],table)
    
    table = [[0.1,0.3,0.5],[0.6,0.2,0.7],[1.5,2.3,0.4]]
    result = funcs.crossout(table,0,0)
    introcs.assert_equals(None,result)
    introcs.assert_float_lists_equal([[0.2,0.7],[2.3,0.4]],table)
   
    table = [[0.1,0.3,0.5],[0.6,0.2,0.7],[1.5,2.3,0.4]]
    result = funcs.crossout(table,2,1)
    introcs.assert_equals(None,result)
    introcs.assert_float_lists_equal([[0.1,0.5],[0.6,0.7]],table)
    
    table = [[0.1,0.3,0.5],[0.6,0.2,0.7],[1.5,2.3,0.4],[0.1,0.2,0.3]]
    result = funcs.crossout(table,1,2)
    introcs.assert_equals(None,result)
    introcs.assert_float_lists_equal([[0.1,0.3],[1.5,2.3],[0.1,0.2]],table)
    
    table = [[0.1,0.3,0.5,1.0],[0.6,0.2,0.7,2.0],[1.5,2.3,0.4,3.0]]
    result = funcs.crossout(table,1,2)
    introcs.assert_equals(None,result)
    introcs.assert_float_lists_equal([[0.1,0.3,1.0],[1.5,2.3,3.0]],table)
    
    table = [[1,2],[3,4]]
    result = funcs.crossout(table,1,0)
    introcs.assert_equals(None,result)
    introcs.assert_float_lists_equal([[2]],table)
    
    table = [[1,2],[3,4]]
    result = funcs.crossout(table,0,1)
    introcs.assert_equals(None,result)
    introcs.assert_float_lists_equal([[3]],table)
    
    table = [[5]]
    result = funcs.crossout(table,0,0)
    introcs.assert_equals(None,result)
    introcs.assert_equals([],table)


def test_place_sums():
    """
    Test procedure for function place_sums().
    
    Note the use of assert_float_lists_equal for testing (nested) lists
    of floats.
    """
    print('Testing place_sums()')
    
    table = [['P1','P3','P5','P7','P9'], [0.7, 0.0, -0.7, 1.0, -0.9]]
    answr = [['P1','P3','P5','P7','P9','Sum'], [0.7, 0.0, -0.7, 1.0, -0.9, 0.1]]
    result = funcs.place_sums(table)
    introcs.assert_equals(None,result)
    # Need to check string part and float part separately
    introcs.assert_equals(answr[0],table[0])
    introcs.assert_float_lists_equal(answr[1:],table[1:])
    
    table = [['P1'], [0.7], [0.1], [0.4], [-0.2], [0.6]]
    answr = [['P1','Sum'], [0.7,0.7], [0.1,0.1], [0.4,0.4], [-0.2,-0.2], [0.6,0.6]]
    result = funcs.place_sums(table)
    introcs.assert_equals(None,result)
    # Need to check string part and float part separately
    introcs.assert_equals(answr[0],table[0])
    introcs.assert_float_lists_equal(answr[1:],table[1:])
   
    table = [['P1','P3','P5'], [0.7, 0.0, -0.7], [0.1, 0.4, -0.6]]
    answr = [['P1','P3','P5','Sum'], [0.7, 0.0, -0.7, 0.0], [0.1, 0.4, -0.6, -0.1]]
    result = funcs.place_sums(table)
    introcs.assert_equals(None,result)
    # Need to check string part and float part separately
    introcs.assert_equals(answr[0],table[0])
    introcs.assert_float_lists_equal(answr[1:],table[1:])
    
    table = [['P1','P3','P5','P7','P9'],
             [0.7, 0.0, -0.7, 1.0, -0.9], 
             [0.1, 0.4, -0.6, 0.9, 0.2],
             [0.4, -0.1, -0.2, 0.1, -0.6], 
             [-0.2, 0.2, 0.2, -0.3, -0.2],
             [0.6, -0.1, -0.0, 0.8, 0.9]]
    answr = [['P1','P3','P5','P7','P9','Sum'],
             [0.7, 0.0, -0.7, 1.0, -0.9, 0.1], 
             [0.1, 0.4, -0.6, 0.9, 0.2, 1.0],
             [0.4, -0.1, -0.2, 0.1, -0.6, -0.4], 
             [-0.2, 0.2, 0.2, -0.3, -0.2, -0.3],
             [0.6, -0.1, -0.0, 0.8, 0.9, 2.2]]
    result = funcs.place_sums(table)
    introcs.assert_equals(None,result)
    # Need to check string part and float part separately
    introcs.assert_equals(answr[0],table[0])
    introcs.assert_float_lists_equal(answr[1:],table[1:])


# Script code
if __name__ == '__main__':
    test_crossout()
    test_place_sums()
    print('Module funcs is working correctly')