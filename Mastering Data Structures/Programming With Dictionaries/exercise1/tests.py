"""  
A completed test script for the dictionary functions.

Author: Walker M. White
Date: August 9, 2019
"""
import funcs
import copy
import introcs


def test_average_grade():
    """
    Test procedure for function average_grade().
    """
    print('Testing average_grade()')
    
    grades = {'wmw2': 55, 'abc3': 90, 'jms45': 86}
    # Snapshot table to make sure we do not modify
    orignl = copy.deepcopy(grades)
    result = funcs.average_grade(grades)
    introcs.assert_floats_equal(77.0,result)
    introcs.assert_equals(orignl,grades)
    
    grades = {'abc123': 0,'abc456':65,'jms457':50}
    # Snapshot table to make sure we do not modify
    orignl = copy.deepcopy(grades)
    result = funcs.average_grade(grades)
    introcs.assert_floats_equal(38.333,result)
    introcs.assert_equals(orignl,grades)
    
    grades = {'abc123': 0,'abc456':65,'jms457':50,'jms123':60,'xyz123':70}
    # Snapshot table to make sure we do not modify
    orignl = copy.deepcopy(grades)
    result = funcs.average_grade(grades)
    introcs.assert_floats_equal(49.0,result)
    introcs.assert_equals(orignl,grades)
    
    grades = {'abc123': 0,'abc456':65,'jms457':50,'jms123':60,'xyz123':70,'xyz456':80,'wmw4':90}
    # Snapshot table to make sure we do not modify
    orignl = copy.deepcopy(grades)
    result = funcs.average_grade(grades)
    introcs.assert_floats_equal(59.286,result)
    introcs.assert_equals(orignl,grades)
    
    grades = {'abc123': 0,'abc456':65,'jms457':50,'jms123':60,'xyz123':70,'xyz456':80,'wmw4':90,'wmw5':100}
    # Snapshot table to make sure we do not modify
    orignl = copy.deepcopy(grades)
    result = funcs.average_grade(grades)
    introcs.assert_floats_equal(64.375,result)
    introcs.assert_equals(orignl,grades)
    
    grades = {'abc123': 0,'abc456':65,'jms457':50,'jms123':60,'xyz123':70,'xyz456':80,'wmw4':90,'wmw5':100,'tor3':88}
    # Snapshot table to make sure we do not modify
    orignl = copy.deepcopy(grades)
    result = funcs.average_grade(grades)
    introcs.assert_floats_equal(67.0,result)
    introcs.assert_equals(orignl,grades)
    
    grades = {'wmw2' : 55, 'abc3' : 90}
    # Snapshot table to make sure we do not modify
    orignl = copy.deepcopy(grades)
    result = funcs.average_grade(grades)
    introcs.assert_floats_equal(72.5,result)
    introcs.assert_equals(orignl,grades)
    
    grades = {'abc3' : 90}
    # Snapshot table to make sure we do not modify
    orignl = copy.deepcopy(grades)
    result = funcs.average_grade(grades)
    introcs.assert_floats_equal(90.0,result)
    introcs.assert_equals(orignl,grades)
    
    grades = {}
    # Snapshot table to make sure we do not modify
    orignl = copy.deepcopy(grades)
    result = funcs.average_grade(grades)
    introcs.assert_floats_equal(0.0,result)
    introcs.assert_equals(orignl,grades)


def test_letter_grades():
    """
    Test procedure for function letter_grades().
    """
    print('Testing letter_grades()')
    
    grades = {'wmw2': 55, 'abc3': 90, 'jms45': 86}
    answer = {'wmw2': 'F', 'abc3': 'A', 'jms45': 'B'}
    # Snapshot table to make sure we do not modify
    orignl = copy.deepcopy(grades)
    result = funcs.letter_grades(grades)
    introcs.assert_equals(answer,result)
    introcs.assert_equals(orignl,grades)
    
    grades = {'abc123': 0,'abc456':65,'jms457':50}
    answer = {'abc123': 'F','abc456':'D','jms457':'F'}
    # Snapshot table to make sure we do not modify
    orignl = copy.deepcopy(grades)
    result = funcs.letter_grades(grades)
    introcs.assert_equals(answer,result)
    introcs.assert_equals(orignl,grades)
    
    grades = {'abc123': 0,'abc456':65,'jms457':50,'jms123':60,'xyz123':70}
    answer = {'abc123': 'F','abc456':'D','jms457':'F','jms123':'D','xyz123':'C'}
    # Snapshot table to make sure we do not modify
    orignl = copy.deepcopy(grades)
    result = funcs.letter_grades(grades)
    introcs.assert_equals(answer,result)
    introcs.assert_equals(orignl,grades)
    
    grades = {'abc123': 0,'abc456':65,'jms457':50,'jms123':60,'xyz123':70,'xyz456':80,'wmw4':90}
    answer = {'abc123': 'F','abc456':'D','jms457':'F','jms123':'D','xyz123':'C','xyz456':'B','wmw4':'A'}
    # Snapshot table to make sure we do not modify
    orignl = copy.deepcopy(grades)
    result = funcs.letter_grades(grades)
    introcs.assert_equals(answer,result)
    introcs.assert_equals(orignl,grades)
    
    grades = {'abc123': 0,'abc456':65,'jms457':50,'jms123':60,'xyz123':70,'xyz456':80,'wmw4':90,'wmw5':100}
    answer = {'abc123': 'F','abc456':'D','jms457':'F','jms123':'D','xyz123':'C','xyz456':'B','wmw4':'A','wmw5':'A'}
    # Snapshot table to make sure we do not modify
    orignl = copy.deepcopy(grades)
    result = funcs.letter_grades(grades)
    introcs.assert_equals(answer,result)
    introcs.assert_equals(orignl,grades)
    
    grades = {'abc123': 0,'abc456':65,'jms457':50,'jms123':60,'xyz123':70,'xyz456':80,'wmw4':90,'wmw5':100,'tor3':88}
    answer = {'abc123': 'F','abc456':'D','jms457':'F','jms123':'D','xyz123':'C','xyz456':'B','wmw4':'A','wmw5':'A','tor3':'B'}
    # Snapshot table to make sure we do not modify
    orignl = copy.deepcopy(grades)
    result = funcs.letter_grades(grades)
    introcs.assert_equals(answer,result)
    introcs.assert_equals(orignl,grades)
    
    grades = {'wmw2' : 55, 'abc3' : 90}
    answer = {'wmw2' : 'F', 'abc3' : 'A'}
    # Snapshot table to make sure we do not modify
    orignl = copy.deepcopy(grades)
    result = funcs.letter_grades(grades)
    introcs.assert_equals(answer,result)
    introcs.assert_equals(orignl,grades)
    
    grades = {'abc3' : 90}
    answer = {'abc3' : 'A'}
    # Snapshot table to make sure we do not modify
    orignl = copy.deepcopy(grades)
    result = funcs.letter_grades(grades)
    introcs.assert_equals(answer,result)
    introcs.assert_equals(orignl,grades)
    
    grades = {}
    answer = {}
    # Snapshot table to make sure we do not modify
    orignl = copy.deepcopy(grades)
    result = funcs.letter_grades(grades)
    introcs.assert_equals(answer,result)
    introcs.assert_equals(orignl,grades)


# Script code
if __name__ == '__main__':
    test_average_grade()
    test_letter_grades()
    print('Module funcs is working correctly')