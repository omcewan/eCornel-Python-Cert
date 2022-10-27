"""  
A completed test script for the dictionary functions.

Author: Walker M. White
Date: August 9, 2019
"""
import funcs
import copy
import introcs


def test_letter_grades():
    """
    Test procedure for function letter_grades().
    """
    print('Testing letter_grades()')
    
    grades = {'wmw2': 55, 'abc3': 90, 'jms45': 86}
    answer = {'wmw2': 'F', 'abc3': 'A', 'jms45': 'B'}
    result = funcs.letter_grades(grades)
    introcs.assert_equals(None,result)
    introcs.assert_equals(answer,grades)
    
    grades = {'abc123': 0,'abc456':65,'jms457':50}
    answer = {'abc123': 'F','abc456':'D','jms457':'F'}
    result = funcs.letter_grades(grades)
    introcs.assert_equals(None,result)
    introcs.assert_equals(answer,grades)
    
    grades = {'abc123': 0,'abc456':65,'jms457':50,'jms123':60,'xyz123':70}
    answer = {'abc123': 'F','abc456':'D','jms457':'F','jms123':'D','xyz123':'C'}
    result = funcs.letter_grades(grades)
    introcs.assert_equals(None,result)
    introcs.assert_equals(answer,grades)
    
    grades = {'abc123': 0,'abc456':65,'jms457':50,'jms123':60,'xyz123':70,'xyz456':80,'wmw4':90}
    answer = {'abc123': 'F','abc456':'D','jms457':'F','jms123':'D','xyz123':'C','xyz456':'B','wmw4':'A'}
    result = funcs.letter_grades(grades)
    introcs.assert_equals(None,result)
    introcs.assert_equals(answer,grades)
    
    grades = {'abc123': 0,'abc456':65,'jms457':50,'jms123':60,'xyz123':70,
              'xyz456':80,'wmw4':90,'wmw5':100}
    answer = {'abc123': 'F','abc456':'D','jms457':'F','jms123':'D',
              'xyz123':'C','xyz456':'B','wmw4':'A','wmw5':'A'}
    result = funcs.letter_grades(grades)
    introcs.assert_equals(None,result)
    introcs.assert_equals(answer,grades)
    
    grades = {'abc123': 0,'abc456':65,'jms457':50,'jms123':60,'xyz123':70,
              'xyz456':80,'wmw4':90,'wmw5':100,'tor3':88}
    answer = {'abc123': 'F','abc456':'D','jms457':'F','jms123':'D',
              'xyz123':'C','xyz456':'B','wmw4':'A','wmw5':'A','tor3':'B'}
    result = funcs.letter_grades(grades)
    introcs.assert_equals(None,result)
    introcs.assert_equals(answer,grades)
    
    grades = {'wmw2' : 55, 'abc3' : 90}
    answer = {'wmw2' : 'F', 'abc3' : 'A'}
    result = funcs.letter_grades(grades)
    introcs.assert_equals(None,result)
    introcs.assert_equals(answer,grades)
    
    grades = {'abc3' : 90}
    answer = {'abc3' : 'A'}
    result = funcs.letter_grades(grades)
    introcs.assert_equals(None,result)
    introcs.assert_equals(answer,grades)
    
    grades = {}
    answer = {}
    result = funcs.letter_grades(grades)
    introcs.assert_equals(None,result)
    introcs.assert_equals(answer,grades)


def test_drop_below():
    """
    Test procedure for function drop_below().
    """
    print('Testing drop_below()')
    
    orignl = {'wmw2': 55, 'abc3': 90, 'jms45': 86}
    grades = {'wmw2': 55, 'abc3': 90, 'jms45': 86}
    answer = {'abc3': 90, 'jms45': 86}
    result = funcs.drop_below(grades,20)
    introcs.assert_equals(None,result)
    introcs.assert_equals(orignl,grades)
    
    result = funcs.drop_below(grades,55)
    introcs.assert_equals(None,result)
    introcs.assert_equals(orignl,grades)
    
    result = funcs.drop_below(grades,60)
    introcs.assert_equals(None,result)
    introcs.assert_equals(answer,grades)
    
    grades = copy.deepcopy(orignl)
    result = funcs.drop_below(grades,86)
    introcs.assert_equals(None,result)
    introcs.assert_equals(answer,grades)
    
    grades = copy.deepcopy(orignl)
    result = funcs.drop_below(grades,95)
    introcs.assert_equals(None,result)
    introcs.assert_equals({},grades)
    
    orignl = {'abc123': 0,'abc456':65,'jms457':50,'jms123':60,'xyz123':70,
              'xyz456':80,'wmw4':90,'wmw5':100,'tor3':88}
    grades = copy.deepcopy(orignl)
    answer = {'xyz456':80,'wmw4':90,'wmw5':100,'tor3':88}
    
    result = funcs.drop_below(grades,0)
    introcs.assert_equals(None,result)
    introcs.assert_equals(orignl,grades)
    
    result = funcs.drop_below(grades,80)
    introcs.assert_equals(None,result)
    introcs.assert_equals(answer,grades)
    
    orignl = {'abc3' : 90}
    grades = {'abc3' : 90}
    result = funcs.drop_below(grades,90)
    introcs.assert_equals(None,result)
    introcs.assert_equals(orignl,grades)
    
    result = funcs.drop_below(grades,100)
    introcs.assert_equals(None,result)
    introcs.assert_equals({},grades)
    
    grades = {}
    result = funcs.drop_below(grades,0)
    introcs.assert_equals(None,result)
    introcs.assert_equals({},grades)


# Script code
if __name__ == '__main__':
    test_letter_grades()
    test_drop_below()
    print('Module funcs is working correctly')