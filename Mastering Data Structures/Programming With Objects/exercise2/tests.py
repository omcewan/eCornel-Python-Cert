"""  
A completed test script for the time functions.

Notice how complicated testing is now.  To test that the return value of a function is
correct, we need to test (1) its type and (2) each attribute separately.  Because 
functions can now modify the arguments, we also need to verify that arguments are not
modified unless the specification specifically says they are.

Author: Walker M. White
Date: August 9, 2019
"""
import funcs
import clock
import introcs


def test_add_time1():
    """
    Test procedure for the function add_time1()
    """
    print('Testing add_time1()')
    
    # TEST 1: Sum 12hr 13min and 13hr 12min
    time1 = clock.Time(12,13)
    time2 = clock.Time(13,12)
    
    result = funcs.add_time1(time1,time2)
    introcs.assert_equals(clock.Time,type(result))
    introcs.assert_equals(25,result.hours)
    introcs.assert_equals(25,result.minutes)
    
    # Verify no objects were modified
    introcs.assert_equals(12,time1.hours)
    introcs.assert_equals(13,time1.minutes)
    introcs.assert_equals(13,time2.hours)
    introcs.assert_equals(12,time2.minutes)
    
    # TEST 2: Sum 1hr 59min and 1hr 2min
    time1 = clock.Time(1,59)
    time2 = clock.Time(3,2)
    
    result = funcs.add_time1(time1,time2)
    introcs.assert_equals(clock.Time,type(result))
    introcs.assert_equals(5,result.hours)
    introcs.assert_equals(1,result.minutes)
    
    # Verify no objects were modified
    introcs.assert_equals(1,time1.hours)
    introcs.assert_equals(59,time1.minutes)
    introcs.assert_equals(3,time2.hours)
    introcs.assert_equals(2,time2.minutes)
    
    # TEST 3: Sum 1hr 15min and 0hr 0min
    time1 = clock.Time(1,15)
    time2 = clock.Time(0,0)
    
    result = funcs.add_time1(time1,time2)
    introcs.assert_equals(clock.Time,type(result))
    introcs.assert_equals(1,result.hours)
    introcs.assert_equals(15,result.minutes)
    
    # Verify no objects were modified
    introcs.assert_equals(1,time1.hours)
    introcs.assert_equals(15,time1.minutes)
    introcs.assert_equals(0,time2.hours)
    introcs.assert_equals(0,time2.minutes)
    
    # Feel free to add more


def test_add_time2():
    """
    Test procedure for the function add_time2()
    """
    print('Testing add_time2()')
    
    # TEST 1: Sum 12hr 13min and 13hr 12min
    time1 = clock.Time(12,13)
    time2 = clock.Time(13,12)
    
    # Verify that nothing is returned
    result = funcs.add_time2(time1,time2)
    introcs.assert_equals(None,result)
    
    # Verify time1 is changed, but time2 is not
    introcs.assert_equals(25,time1.hours)
    introcs.assert_equals(25,time1.minutes)
    introcs.assert_equals(13,time2.hours)
    introcs.assert_equals(12,time2.minutes)
    
    # TEST 2: Sum 1hr 59min and 1hr 2min
    time1 = clock.Time(1,59)
    time2 = clock.Time(3,2)
    
    # Verify that nothing is returned
    result = funcs.add_time2(time1,time2)
    introcs.assert_equals(None,result)
    
    # Verify time1 is changed, but time2 is not
    introcs.assert_equals(5,time1.hours)
    introcs.assert_equals(1,time1.minutes)
    introcs.assert_equals(3,time2.hours)
    introcs.assert_equals(2,time2.minutes)
    
    # TEST 3: Sum 1hr 15min and 0hr 0min
    time1 = clock.Time(1,15)
    time2 = clock.Time(0,0)
    
    # Verify that nothing is returned
    result = funcs.add_time2(time1,time2)
    introcs.assert_equals(None,result)
    
    # Verify that objects are correct
    introcs.assert_equals(1,time1.hours)
    introcs.assert_equals(15,time1.minutes)
    introcs.assert_equals(0,time2.hours)
    introcs.assert_equals(0,time2.minutes)
    
    # Feel free to add more


if __name__ == '__main__':
    test_add_time1()
    test_add_time2()
    print('Module funcs passed all tests.')