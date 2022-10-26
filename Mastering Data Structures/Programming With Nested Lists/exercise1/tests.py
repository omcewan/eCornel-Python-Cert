"""  
A completed test script for the nested list functions.

Author: Walker M. White
Date: August 9, 2019
"""
import funcs
import introcs
import copy


def test_row_sums():
    """
    Test procedure for function row_sums().
    
    Note the use of assert_float_lists_equal for testing (nested) lists
    of floats.
    """
    print('Testing row_sums()')
    
    table = [[0.7, 0.0, -0.7, 1.0, -0.9]]
    # Snapshot table to make sure we do not modify
    orig = copy.deepcopy(table)
    result = funcs.row_sums(table)
    introcs.assert_float_lists_equal([0.1],result)
    introcs.assert_float_lists_equal(orig,table)
    
    table = [[0.7], [0.1], [0.4], [-0.2], [0.6]]
    # Snapshot table to make sure we do not modify
    orig = copy.deepcopy(table)
    result = funcs.row_sums(table)
    introcs.assert_float_lists_equal([0.7, 0.1, 0.4, -0.2, 0.6],result)
    introcs.assert_float_lists_equal(orig,table)
   
    table = [[0.7, 0.0, -0.7], [0.1, 0.4, -0.6]]    
    # Snapshot table to make sure we do not modify
    orig = copy.deepcopy(table)
    result = funcs.row_sums(table)
    introcs.assert_float_lists_equal([0.0, -0.1],result)
    introcs.assert_float_lists_equal(orig,table)
    
    table = [[0.7, 0.0, -0.7, 1.0, -0.9], 
             [0.1, 0.4, -0.6, 0.9, 0.2],
             [0.4, -0.1, -0.2, 0.1, -0.6], 
             [-0.2, 0.2, 0.2, -0.3, -0.2],
             [0.6, -0.1, -0.0, 0.8, 0.9]]
    # Snapshot table to make sure we do not modify
    orig = copy.deepcopy(table)
    result = funcs.row_sums(table)
    introcs.assert_float_lists_equal([0.1, 1.0, -0.4, -0.3, 2.2],result)
    introcs.assert_float_lists_equal(orig,table)


def test_crossout():
    """
    Test procedure for function crossout().
    
    Note the use of assert_float_lists_equal for testing (nested) lists
    of floats.
    """
    print('Testing crossout()')
    
    table = [[0.1,0.3,0.5],[0.6,0.2,0.7],[1.5,2.3,0.4]]
    # Snapshot table to make sure we do not modify
    orig = copy.deepcopy(table)
    result = funcs.crossout(table,1,2)
    introcs.assert_float_lists_equal([[0.1,0.3],[1.5,2.3]],result)
    introcs.assert_float_lists_equal(orig,table)
    
    result = funcs.crossout(table,0,0)
    introcs.assert_float_lists_equal([[0.2,0.7],[2.3,0.4]],result)
    introcs.assert_float_lists_equal(orig,table)
   
    result = funcs.crossout(table,2,1)
    introcs.assert_float_lists_equal([[0.1,0.5],[0.6,0.7]],result)
    introcs.assert_float_lists_equal(orig,table)
    
    table = [[0.1,0.3,0.5],[0.6,0.2,0.7],[1.5,2.3,0.4],[0.1,0.2,0.3]]
    # Snapshot table to make sure we do not modify
    orig = copy.deepcopy(table)
    result = funcs.crossout(table,1,2)
    introcs.assert_float_lists_equal([[0.1,0.3],[1.5,2.3],[0.1,0.2]],result)
    introcs.assert_float_lists_equal(orig,table)
    
    table = [[0.1,0.3,0.5,1.0],[0.6,0.2,0.7,2.0],[1.5,2.3,0.4,3.0]]
    # Snapshot table to make sure we do not modify
    orig = copy.deepcopy(table)
    result = funcs.crossout(table,1,2)
    introcs.assert_float_lists_equal([[0.1,0.3,1.0],[1.5,2.3,3.0]],result)
    introcs.assert_float_lists_equal(orig,table)
    
    table = [[1,2],[3,4]]
    # Snapshot table to make sure we do not modify
    orig = copy.deepcopy(table)
    result = funcs.crossout(table,1,0)
    introcs.assert_float_lists_equal([[2]],result)
    introcs.assert_float_lists_equal(orig,table)
    
    result = funcs.crossout(table,0,1)
    introcs.assert_float_lists_equal([[3]],result)
    introcs.assert_float_lists_equal(orig,table)
    
    table = [[5]]
    # Snapshot table to make sure we do not modify
    orig = copy.deepcopy(table)
    result = funcs.crossout(table,0,0)
    introcs.assert_equals([],result)
    introcs.assert_float_lists_equal(orig,table)


# Script code
if __name__ == '__main__':
    test_row_sums()
    test_crossout()
    print('Module funcs is working correctly')