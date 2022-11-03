"""  
A completed test script for the module funcs

Author: Walker M. White
Date: November 30, 2019
"""
import funcs
import introcs
import os.path


def test_count_lines():
    """
    Test procedure for the function count_lines()
    """
    print('Testing count_lines()')
    
    # Find the directory with this file in it
    parent = os.path.split(__file__)[0]
    
    # Remaining files are in 'files' folder, relative to this one
    filepath = os.path.join(parent,'files','readfile1.txt')
    result = funcs.count_lines(filepath)
    introcs.assert_equals(6,result)
    
    filepath = os.path.join(parent,'files','readfile2.txt')
    result = funcs.count_lines(filepath)
    introcs.assert_equals(23,result)
    
    filepath = os.path.join(parent,'files','readfile3.txt')
    result = funcs.count_lines(filepath)
    introcs.assert_equals(10,result)


def test_write_numbers():
    """
    Test procedure for the function write_numbers()
    """
    print('Testing write_numbers()')
    
    # Find the directory with this file in it
    parent = os.path.split(__file__)[0]
    
    # Remaining files are in 'files' folder, relative to this one
    
    # TEST 1
    filepath = os.path.join(parent,'files','tempfile.txt')
    funcs.write_numbers(filepath,5)
    
    # Check file was created
    introcs.assert_true(os.path.exists(filepath))
    
    file = open(filepath)
    actual  =  file.read()
    file.close()
    
    file = open(os.path.join(parent,'files','writefile1.txt'))
    correct = file.read()
    file.close()
    
    # Check to see if they are the same
    introcs.assert_equals(correct,actual)
    
    # TEST 2
    filepath = os.path.join(parent,'files','tempfile.txt')
    funcs.write_numbers(filepath,16)
    
    # Check file was created
    introcs.assert_true(os.path.exists(filepath))
    
    file = open(filepath)
    actual  =  file.read()
    file.close()
    
    file = open(os.path.join(parent,'files','writefile2.txt'))
    correct = file.read()
    file.close()
    
    # Check to see if they are the same
    introcs.assert_equals(correct,actual)
    
    # TEST 3
    filepath = os.path.join(parent,'files','tempfile.txt')
    funcs.write_numbers(filepath,26)
    
    # Check file was created
    introcs.assert_true(os.path.exists(filepath))
    
    file = open(filepath)
    actual  =  file.read()
    file.close()
    
    file = open(os.path.join(parent,'files','writefile3.txt'))
    correct = file.read()
    file.close()
    
    # Check to see if they are the same
    introcs.assert_equals(correct,actual)


if __name__ == '__main__':
    test_count_lines()
    test_write_numbers()
    print('Module funcs passed all tests.')