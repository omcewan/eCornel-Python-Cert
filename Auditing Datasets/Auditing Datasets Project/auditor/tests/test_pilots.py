"""
Test procedures for the pilot functions for this project.

These tests read from the pilot file in the same directory as this one.

Author: Walker M. White (wmw2)
Date:   June 7, 2019
"""
# See: https://stackoverflow.com/questions/14132789/relative-imports-for-the-billionth-time
if __package__ is None or __package__ == '':
    # Access the module if run from __main__.py (Script visibility)
    from support import *
else:
    # Access the module if run from __init__.py (Packages visibility)
    from .support import *


# Load the utils modle
utils  = load_from_path('utils')
pilots = load_from_path('pilots')
import datetime

# Test the REQUIRE functionality (weather)
TEST_BASIC_APP   = 0
# Test the first extension (endorsements and certification and pilot functions)
TEST_EXTENSION_1 = 1
# Test the second extension (repairs)
TEST_EXTENSION_2 = 2

def cert_to_name(cert):
    """
    Returns a string describing a certification.
    
    Parameter cert: The certification
    Precondition: cert is an int and one of PILOT_INVALID, PILOT_NOVICE, PILOT_STUDENT,
    PILOT_CERTIFIED, PILOT_50_HOURS
    """
    if cert == pilots.PILOT_INVALID:
        return 'PILOT_INVALID'
    elif cert == pilots.PILOT_NOVICE:
        return 'PILOT_NOVICE'
    elif cert == pilots.PILOT_STUDENT:
        return 'PILOT_STUDENT'
    elif cert == pilots.PILOT_CERTIFIED:
        return 'PILOT_CERTIFIED'
    elif cert == pilots.PILOT_50_HOURS:
        return 'PILOT_50_HOURS'
    return cert


def test_get_certification():
    """
    Tests the function pilots.get_certification
    """
    fcn = 'pilots.get_certification'
    
    # Access the file relative to this one, not the user's terminal
    parent = os.path.split(__file__)[0]
    fpath  = os.path.join(parent,'students.csv')
    table = utils.read_csv(fpath)
    
    # TEST CASES
    takeoffs = ['2015-01-14T08:00:00','2015-07-15T10:15:20','2015-07-16T10:15:20',
                '2015-10-08T12:30:45','2016-02-15T20:35:16','2017-12-30 16:30:45']
    students = {'S00313' : ( 0,1,1,1,1,1),
                'S00331' : (-1,0,0,0,1,1),
                'S00353' : (-1,2,2,3,3,3),
                'S00362' : (-1,1,1,2,3,3),
                'S00378' : (-1,0,1,2,3,3),
                'S01139' : (-1,-1,-1,-1,-1,0)}
    
    # CHECK THE TEST CASES
    for person in students:
        for pos in range(len(takeoffs)):
            row  = utils.get_for_id(person,table)
            time = utils.str_to_time(takeoffs[pos], "America/New_York")
            cert = pilots.get_certification(time,row)
            data = (fcn,person,repr(cert_to_name(cert)),takeoffs[pos],repr(cert_to_name(students[person][pos])))
            assert_equals(students[person][pos], cert,
              '%s marked %s as %s on %s, but was really %s' % data)
    
    print('  %s passed all tests' % fcn)


def test_has_instrument_rating():
    """
    Tests the function pilots.has_instrument_rating
    """
    fcn = 'pilots.has_instrument_rating'
    
    # Access the file relative to this one, not the user's terminal
    parent = os.path.split(__file__)[0]
    fpath  = os.path.join(parent,'students.csv')
    table = utils.read_csv(fpath)
    
    # TEST CASES
    takeoffs = ['2015-12-11T08:00:00','2015-12-27T10:15:20','2015-12-28T10:15:20','2016-04-18T12:30:45']
    students = {'S00313' : ( False, False, False, False),
                'S00350' : ( False, True, True, True),
                'S00369' : ( False, False, True, True),
                'S00378' : ( False, False, False, True)}
    
    # CHECK THE TEST CASES
    for person in students:
        for pos in range(len(takeoffs)):
            row  = utils.get_for_id(person,table)
            time = utils.str_to_time(takeoffs[pos])
            rate = pilots.has_instrument_rating(time,row)
            data = (fcn,person,repr(rate),takeoffs[pos],repr(students[person][pos]))
            assert_equals(students[person][pos], rate,
              '%s marked %s as %s on %s, but was really %s' % data)
    
    print('  %s passed all tests' % fcn)


def test_has_advanced_endorsement():
    """
    Tests the function pilots.has_advanced_endorsement
    """
    fcn = 'pilots.has_advanced_endorsement'
    
    parent = os.path.split(__file__)[0]
    fpath  = os.path.join(parent,'students.csv')
    table = utils.read_csv(fpath)
    
    # TEST CASES
    takeoffs = ['2015-12-20T08:00:00','2016-05-31T10:15:20','2016-12-05T12:30:45','2016-12-12T10:15:20',]
    students = {'S00313' : ( False, False, False, False),
                'S00369' : ( False, False, False, False),
                'S00378' : ( False, True, True, True),
                'S00436' : ( False, False, True, True),
                'S00536' : ( False, False, False, True)}
    
    # CHECK THE TEST CASES
    for row in table[1:]:
        if row[0] in students:
            for pos in range(len(takeoffs)):
                time = utils.str_to_time(takeoffs[pos])
                rate = pilots.has_advanced_endorsement(time,row)
                data = (fcn,row[0],repr(rate),takeoffs[pos],repr(students[row[0]][pos]))
                assert_equals(students[row[0]][pos], rate,
                  '%s marked %s as %s on %s, but was really %s' % data)
    
    print('  %s passed all tests' % fcn)


def test_has_multiengine_endorsement():
    """
    Tests the function pilots.has_multiengine_endorsement
    """
    fcn = 'pilots.has_multiengine_endorsement'
    
    parent = os.path.split(__file__)[0]
    fpath  = os.path.join(parent,'students.csv')
    table = utils.read_csv(fpath)
    
    # TEST CASES
    takeoffs = ['2015-12-11T08:00:00','2017-09-27T10:15:20','2017-09-28T10:15:20','2017-11-05T12:30:45']
    students = {'S00313' : ( False, False, False, False),
                'S00378' : ( False, False, True, True),
                'S00436' : ( False, False, False, True),
                'S00536' : ( False, False, False, False) }
    
    # CHECK THE TEST CASES
    for row in table[1:]:
        if row[0] in students:
            for pos in range(len(takeoffs)):
                time = utils.str_to_time(takeoffs[pos])
                rate = pilots.has_multiengine_endorsement(time,row)
                data = (fcn,row[0],repr(rate),takeoffs[pos],repr(students[row[0]][pos]))
                assert_equals(students[row[0]][pos], rate,
                  '%s marked %s as %s on %s, but was really %s' % data)
    
    print('  %s passed all tests' % fcn)


def test_get_best_value():
    """
    Tests the function pilots.get_best_value
    """
    fcn = 'pilots.get_best_value'
    
    # Test the minimums table
    parent = os.path.split(__file__)[0]
    fpath  = os.path.join(parent,'minimums.csv')
    table = utils.read_csv(fpath)[1:]
    
    # TEST CASES
    # Expected answers for each of the indicated columns
    tests = { 4: (500.0, 5000.0),
              5: (0.75, 10.0),
              6: (20.0, 30.0),
              7: (8.0, 20.0) }
    # Check for both True (highest) and False (lowest)
    situations = ( (False, 0, 'lowest'),
                   (True, 1, 'highest') )
    
    # CHECK THE TEST CASES
    for col, bests in tests.items():
        for situ in situations:
            best = pilots.get_best_value(table, col, situ[0])
            data = (fcn, repr(best), situ[2], col, bests[situ[1]])
            assert_floats_equal(bests[situ[1]], best,
                '%s returned %s as %s value for column position %s in minimums.csv, but should have returned %s' % data)

    print('  %s passed all tests' % fcn)


def test_get_minimums():
    """
    Tests the function pilots.get_minimums
    """
    fcn = 'pilots.get_minimums'
    
    # Test the standard table
    parent = os.path.split(__file__)[0]
    fpath  = os.path.join(parent,'minimums.csv')
    table = utils.read_csv(fpath)
    
    # TEST CASES (last element of each tuple is the row in the minimums table)
    testcases = [(pilots.PILOT_INVALID,  'Pattern',      False,False,True, table,None),
                 (pilots.PILOT_INVALID,  'Pattern',      True, False,True, table,21),
                 (pilots.PILOT_NOVICE,   'Pattern',      False,False,True, table,None),
                 (pilots.PILOT_NOVICE,   'Pattern',      True, False,True, table,21),
                 (pilots.PILOT_STUDENT,  'Pattern',      False,False,True, table,None),
                 (pilots.PILOT_STUDENT,  'Practice Area',False,False,True, table,None),
                 (pilots.PILOT_STUDENT,  'Cross Country',False,False,True, table,None),
                 (pilots.PILOT_STUDENT,  'Pattern',      False,True, True, table,1),
                 (pilots.PILOT_STUDENT,  'Practice Area',False,True, True, table,2),
                 (pilots.PILOT_STUDENT,  'Cross Country',False,True, True, table,3),
                 (pilots.PILOT_STUDENT,  'Pattern',      False,False,False,table,None),
                 (pilots.PILOT_STUDENT,  'Practice Area',False,False,False,table,None),
                 (pilots.PILOT_STUDENT,  'Cross Country',False,False,False,table,None),
                 (pilots.PILOT_STUDENT,  'Pattern',      False,True, False,table,None),
                 (pilots.PILOT_STUDENT,  'Practice Area',False,True, False,table,None),
                 (pilots.PILOT_STUDENT,  'Cross Country',False,True, False,table,None),
                 (pilots.PILOT_STUDENT,  'Pattern',      True,False,True, table,21),
                 (pilots.PILOT_STUDENT,  'Practice Area',True,False,True, table,21),
                 (pilots.PILOT_STUDENT,  'Cross Country',True,False,True, table,21),
                 (pilots.PILOT_STUDENT,  'Pattern',      True,True, True, table,14),
                 (pilots.PILOT_STUDENT,  'Practice Area',True,True, True, table,15),
                 (pilots.PILOT_STUDENT,  'Cross Country',True,True, True, table,16),
                 (pilots.PILOT_STUDENT,  'Pattern',      True,False,False,table,22),
                 (pilots.PILOT_STUDENT,  'Practice Area',True,False,False,table,22),
                 (pilots.PILOT_STUDENT,  'Cross Country',True,False,False,table,22),
                 (pilots.PILOT_STUDENT,  'Pattern',      True,True, False,table,17),
                 (pilots.PILOT_STUDENT,  'Practice Area',True,True, False,table,17),
                 (pilots.PILOT_STUDENT,  'Cross Country',True,True, False,table,18),
                 (pilots.PILOT_CERTIFIED,'Pattern',      False,False,True, table,19),
                 (pilots.PILOT_CERTIFIED,'Practice Area',False,False,True, table,19),
                 (pilots.PILOT_CERTIFIED,'Cross Country',False,False,True, table,19),
                 (pilots.PILOT_CERTIFIED,'Pattern',      False,True, True, table,4),
                 (pilots.PILOT_CERTIFIED,'Practice Area',False,True, True, table,5),
                 (pilots.PILOT_CERTIFIED,'Cross Country',False,True, True, table,6),
                 (pilots.PILOT_CERTIFIED,'Pattern',      False,False,False,table,20),
                 (pilots.PILOT_CERTIFIED,'Practice Area',False,False,False,table,20),
                 (pilots.PILOT_CERTIFIED,'Cross Country',False,False,False,table,20),
                 (pilots.PILOT_CERTIFIED,'Pattern',      False,True, False,table,7),
                 (pilots.PILOT_CERTIFIED,'Practice Area',False,True, False,table,7),
                 (pilots.PILOT_CERTIFIED,'Cross Country',False,True, False,table,8),
                 (pilots.PILOT_CERTIFIED,'Pattern',      True,False,True, table,21),
                 (pilots.PILOT_CERTIFIED,'Practice Area',True,False,True, table,21),
                 (pilots.PILOT_CERTIFIED,'Cross Country',True,False,True, table,21),
                 (pilots.PILOT_CERTIFIED,'Pattern',      True,True, True, table,14),
                 (pilots.PILOT_CERTIFIED,'Practice Area',True,True, True, table,15),
                 (pilots.PILOT_CERTIFIED,'Cross Country',True,True, True, table,16),
                 (pilots.PILOT_CERTIFIED,'Pattern',      True,False,False,table,22),
                 (pilots.PILOT_CERTIFIED,'Practice Area',True,False,False,table,22),
                 (pilots.PILOT_CERTIFIED,'Cross Country',True,False,False,table,22),
                 (pilots.PILOT_CERTIFIED,'Pattern',      True,True, False,table,17),
                 (pilots.PILOT_CERTIFIED,'Practice Area',True,True, False,table,17),
                 (pilots.PILOT_CERTIFIED,'Cross Country',True,True, False,table,18),
                 (pilots.PILOT_50_HOURS, 'Pattern',      False,False,True, table,19),
                 (pilots.PILOT_50_HOURS, 'Practice Area',False,False,True, table,19),
                 (pilots.PILOT_50_HOURS, 'Cross Country',False,False,True, table,19),
                 (pilots.PILOT_50_HOURS, 'Pattern',      False,True, True, table,9),
                 (pilots.PILOT_50_HOURS, 'Practice Area',False,True, True, table,10),
                 (pilots.PILOT_50_HOURS, 'Cross Country',False,True, True, table,11),
                 (pilots.PILOT_50_HOURS, 'Pattern',      False,False,False,table,20),
                 (pilots.PILOT_50_HOURS, 'Practice Area',False,False,False,table,20),
                 (pilots.PILOT_50_HOURS, 'Cross Country',False,False,False,table,20),
                 (pilots.PILOT_50_HOURS, 'Pattern',      False,True, False,table,12),
                 (pilots.PILOT_50_HOURS, 'Practice Area',False,True, False,table,12),
                 (pilots.PILOT_50_HOURS, 'Cross Country',False,True, False,table,13),
                 (pilots.PILOT_50_HOURS, 'Pattern',      True,False,True, table,21),
                 (pilots.PILOT_50_HOURS, 'Practice Area',True,False,True, table,21),
                 (pilots.PILOT_50_HOURS, 'Cross Country',True,False,True, table,21),
                 (pilots.PILOT_50_HOURS, 'Pattern',      True,True, True, table,14),
                 (pilots.PILOT_50_HOURS, 'Practice Area',True,True, True, table,15),
                 (pilots.PILOT_50_HOURS, 'Cross Country',True,True, True, table,16),
                 (pilots.PILOT_50_HOURS, 'Pattern',      True,False,False,table,22),
                 (pilots.PILOT_50_HOURS, 'Practice Area',True,False,False,table,22),
                 (pilots.PILOT_50_HOURS, 'Cross Country',True,False,False,table,22),
                 (pilots.PILOT_50_HOURS, 'Pattern',      True,True, False,table,17),
                 (pilots.PILOT_50_HOURS, 'Practice Area',True,True, False,table,17),
                 (pilots.PILOT_50_HOURS, 'Cross Country',True,True, False,table,18)]
    
    # CHECK THE TEST CASES
    for test in testcases:
        mins = pilots.get_minimums(*test[:-1])
        expt = None if test[-1] is None else list(map(float,table[test[-1]][4:]))
        data = (fcn,'('+','.join(map(repr,test[:-2]))+',minimums)',repr(mins),repr(expt))
        if expt:
            assert_float_lists_equal(expt, mins,'%s%s returned %s, but should have returned %s' % data)
        else:
            assert_equals(expt, mins,'%s%s returned %s, but should have returned %s' % data)
    
    # Test the alternates to catch hard-coding
    parent = os.path.split(__file__)[0]
    fpath  = os.path.join(parent,'alternates.csv')
    table = utils.read_csv(fpath)
    
    # TEST CASES (last element of each tuple is the row in the minimums table)
    testcases = [(pilots.PILOT_INVALID,  'Pattern',      False,False,True, table,None),
                 (pilots.PILOT_INVALID,  'Pattern',      True, False,True, table,3),
                 (pilots.PILOT_NOVICE,   'Pattern',      False,False,True, table,None),
                 (pilots.PILOT_NOVICE,   'Pattern',      True, False,True, table,3),
                 (pilots.PILOT_STUDENT,  'Pattern',      False,False,True, table,None),
                 (pilots.PILOT_STUDENT,  'Practice Area',False,False,True, table,None),
                 (pilots.PILOT_STUDENT,  'Cross Country',False,False,True, table,None),
                 (pilots.PILOT_STUDENT,  'Pattern',      False,True, True, table,10),
                 (pilots.PILOT_STUDENT,  'Practice Area',False,True, True, table,8),
                 (pilots.PILOT_STUDENT,  'Cross Country',False,True, True, table,11),
                 (pilots.PILOT_STUDENT,  'Pattern',      False,False,False,table,None),
                 (pilots.PILOT_STUDENT,  'Practice Area',False,False,False,table,None),
                 (pilots.PILOT_STUDENT,  'Cross Country',False,False,False,table,None),
                 (pilots.PILOT_STUDENT,  'Pattern',      False,True, False,table,None),
                 (pilots.PILOT_STUDENT,  'Practice Area',False,True, False,table,None),
                 (pilots.PILOT_STUDENT,  'Cross Country',False,True, False,table,None),
                 (pilots.PILOT_STUDENT,  'Pattern',      True,False,True, table,3),
                 (pilots.PILOT_STUDENT,  'Practice Area',True,False,True, table,3),
                 (pilots.PILOT_STUDENT,  'Cross Country',True,False,True, table,3),
                 (pilots.PILOT_STUDENT,  'Pattern',      True,True, True, table,15),
                 (pilots.PILOT_STUDENT,  'Practice Area',True,True, True, table,16),
                 (pilots.PILOT_STUDENT,  'Cross Country',True,True, True, table,9),
                 (pilots.PILOT_STUDENT,  'Pattern',      True,False,False,table,4),
                 (pilots.PILOT_STUDENT,  'Practice Area',True,False,False,table,4),
                 (pilots.PILOT_STUDENT,  'Cross Country',True,False,False,table,4),
                 (pilots.PILOT_STUDENT,  'Pattern',      True,True, False,table,19),
                 (pilots.PILOT_STUDENT,  'Practice Area',True,True, False,table,19),
                 (pilots.PILOT_STUDENT,  'Cross Country',True,True, False,table,20),
                 (pilots.PILOT_CERTIFIED,'Pattern',      False,False,True, table,21),
                 (pilots.PILOT_CERTIFIED,'Practice Area',False,False,True, table,21),
                 (pilots.PILOT_CERTIFIED,'Cross Country',False,False,True, table,21),
                 (pilots.PILOT_CERTIFIED,'Pattern',      False,True, True, table,1),
                 (pilots.PILOT_CERTIFIED,'Practice Area',False,True, True, table,2),
                 (pilots.PILOT_CERTIFIED,'Cross Country',False,True, True, table,5),
                 (pilots.PILOT_CERTIFIED,'Pattern',      False,False,False,table,22),
                 (pilots.PILOT_CERTIFIED,'Practice Area',False,False,False,table,22),
                 (pilots.PILOT_CERTIFIED,'Cross Country',False,False,False,table,22),
                 (pilots.PILOT_CERTIFIED,'Pattern',      False,True, False,table,6),
                 (pilots.PILOT_CERTIFIED,'Practice Area',False,True, False,table,6),
                 (pilots.PILOT_CERTIFIED,'Cross Country',False,True, False,table,7),
                 (pilots.PILOT_CERTIFIED,'Pattern',      True,False,True, table,3),
                 (pilots.PILOT_CERTIFIED,'Practice Area',True,False,True, table,3),
                 (pilots.PILOT_CERTIFIED,'Cross Country',True,False,True, table,3),
                 (pilots.PILOT_CERTIFIED,'Pattern',      True,True, True, table,15),
                 (pilots.PILOT_CERTIFIED,'Practice Area',True,True, True, table,16),
                 (pilots.PILOT_CERTIFIED,'Cross Country',True,True, True, table,9),
                 (pilots.PILOT_CERTIFIED,'Pattern',      True,False,False,table,4),
                 (pilots.PILOT_CERTIFIED,'Practice Area',True,False,False,table,4),
                 (pilots.PILOT_CERTIFIED,'Cross Country',True,False,False,table,4),
                 (pilots.PILOT_CERTIFIED,'Pattern',      True,True, False,table,19),
                 (pilots.PILOT_CERTIFIED,'Practice Area',True,True, False,table,19),
                 (pilots.PILOT_CERTIFIED,'Cross Country',True,True, False,table,20),
                 (pilots.PILOT_50_HOURS, 'Pattern',      False,False,True, table,21),
                 (pilots.PILOT_50_HOURS, 'Practice Area',False,False,True, table,21),
                 (pilots.PILOT_50_HOURS, 'Cross Country',False,False,True, table,21),
                 (pilots.PILOT_50_HOURS, 'Pattern',      False,True, True, table,12),
                 (pilots.PILOT_50_HOURS, 'Practice Area',False,True, True, table,17),
                 (pilots.PILOT_50_HOURS, 'Cross Country',False,True, True, table,18),
                 (pilots.PILOT_50_HOURS, 'Pattern',      False,False,False,table,22),
                 (pilots.PILOT_50_HOURS, 'Practice Area',False,False,False,table,22),
                 (pilots.PILOT_50_HOURS, 'Cross Country',False,False,False,table,22),
                 (pilots.PILOT_50_HOURS, 'Pattern',      False,True, False,table,13),
                 (pilots.PILOT_50_HOURS, 'Practice Area',False,True, False,table,13),
                 (pilots.PILOT_50_HOURS, 'Cross Country',False,True, False,table,14),
                 (pilots.PILOT_50_HOURS, 'Pattern',      True,False,True, table,3),
                 (pilots.PILOT_50_HOURS, 'Practice Area',True,False,True, table,3),
                 (pilots.PILOT_50_HOURS, 'Cross Country',True,False,True, table,3),
                 (pilots.PILOT_50_HOURS, 'Pattern',      True,True, True, table,15),
                 (pilots.PILOT_50_HOURS, 'Practice Area',True,True, True, table,16),
                 (pilots.PILOT_50_HOURS, 'Cross Country',True,True, True, table,9),
                 (pilots.PILOT_50_HOURS, 'Pattern',      True,False,False,table,4),
                 (pilots.PILOT_50_HOURS, 'Practice Area',True,False,False,table,4),
                 (pilots.PILOT_50_HOURS, 'Cross Country',True,False,False,table,4),
                 (pilots.PILOT_50_HOURS, 'Pattern',      True,True, False,table,19),
                 (pilots.PILOT_50_HOURS, 'Practice Area',True,True, False,table,19),
                 (pilots.PILOT_50_HOURS, 'Cross Country',True,True, False,table,20)]
    
    # CHECK THE TEST CASES
    for test in testcases:
        mins = pilots.get_minimums(*test[:-1])
        expt = None if test[-1] is None else list(map(float,table[test[-1]][4:]))
        data = (fcn,'('+','.join(map(repr,test[:-2]))+',alternates)',repr(mins),repr(expt))
        if expt:
            assert_float_lists_equal(expt, mins,'%s%s returned %s, but should have returned %s' % data)
        else:
            assert_equals(expt, mins,'%s%s returned %s, but should have returned %s' % data)
    
    print('  %s passed all tests' % fcn)


def test(level=TEST_BASIC_APP):
    """
    Performs all tests on the module pilots.
    """
    print('Testing module pilots')
    test_get_certification()
    if level >= TEST_EXTENSION_1:
        test_has_instrument_rating()
        test_has_advanced_endorsement()
        test_has_multiengine_endorsement()
    test_get_best_value()
    test_get_minimums()
