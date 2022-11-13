"""
Test procedures for the violation functions for this project.

These tests read from the input files in the same directory as this one.

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
violations = load_from_path('violations')


def flight_type(lesson,students):
    """
    Returns a message with the information about this flight type.
    
    Most problems with list_weather_violations are incorrectly gathering minimums.
    Hopefully this error message helps with that.
    """
    indx = pilots.get_certification(utils.str_to_time(lesson[3]),
                                    utils.get_for_id(lesson[0],students))
    cert = ['a novice pilot','a student pilot','a certified pilot',
            'a pilot with 50 hours experience','a unregistered pilot'][indx]
    sups = "dual instruction" if lesson[2] else cert
    cond = 'VMC' if lesson[5] == 'VFR' else 'IMC'
    return 'This is a %s flight with %s in %s conditions.' % (lesson[6],sups,cond)


def test_bad_visibility():
    """
    Tests the function bad_visibility
    """
    fcn = 'violations.bad_visibility'
    
    parent = os.path.split(__file__)[0]
    fpath  = os.path.join(parent,'weather.json')
    report = utils.read_json(fpath)
    
    minimums = [0.75,1,2,3,5,8,10]
    keys = [("2017-12-31T15:00:00-05:00",6), ("2017-12-31T14:00:00-05:00",2),
            ('2017-12-31T13:00:00-05:00',0), ('2017-12-30T09:00:00-05:00',1),
            ('2018-01-01T00:00:00-05:00',2), ('2017-12-31T01:00:00-05:00',3),
            ('2017-12-31T22:00:00-05:00',4), ('2017-12-31T03:00:00-05:00',5),
            ('2016-12-31T01:00:00-05:00',0),('2017-12-31T21:00:00-05:00',-1)]
    
    # Perform the tests
    for key in keys:
        visibility = report[key[0]]['visibility']
        for pos in range(len(minimums)):
            expt = key[1] != -1 and key[1] <= pos
            test = violations.bad_visibility(visibility,minimums[pos])
            data = (fcn,repr(visibility),repr(minimums[pos]),repr(test),repr(expt))
            assert_equals(expt, test,'%s(%s,%s) returned %s, but should have returned %s' % data)
    
    print('  %s passed all tests' % fcn)


def test_bad_winds():
    """
    Tests the function bad_winds
    """
    fcn = 'violations.bad_winds'
    
    parent = os.path.split(__file__)[0]
    fpath  = os.path.join(parent,'weather.json')
    report = utils.read_json(fpath)
    
    minimums = [(30,20),(25,15),(20,10),(20,8),(10,5)]
    keys =[("2017-06-20T13:00:00-04:00",0), ('2017-12-25T13:00:00-05:00',0), 
           ('2017-12-25T15:00:00-05:00',1), ('2017-12-30T21:00:00-05:00',2),
           ('2017-12-31T20:00:00-05:00',3), ('2018-01-01T00:00:00-05:00',4),
           ('2017-12-31T06:00:00-05:00',5), ("2017-10-12T11:00:00-04:00",0),
           ('2017-05-09T07:00:00-04:00',5) ]
    
    # Perform the tests
    for key in keys:
        winds = report[key[0]]['wind']
        for pos in range(len(minimums)):
            expt = key[1] != -1 and key[1] <= pos
            test = violations.bad_winds(winds,*minimums[pos])
            data = (fcn,repr(winds),repr(minimums[pos][0]),repr(minimums[pos][1]),repr(test),repr(expt))
            assert_equals(expt, test,'%s(%s,%s,%s) returned %s, but should have returned %s' % data)
    
    print('  %s passed all tests' % fcn)


def test_bad_ceiling():
    """
    Tests the function bad_ceiling
    """
    fcn = 'violations.bad_ceiling'
    
    parent = os.path.split(__file__)[0]
    fpath  = os.path.join(parent,'weather.json')
    report = utils.read_json(fpath)
    
    minimums = [500,1000,1500,2000,2500,3000,3500,5000]
    keys =[("2017-12-30T19:00:00-05:00",-1),("2017-10-31T12:00:00-04:00",0),
           ('2017-12-23T22:00:00-05:00',0), ('2017-12-31T12:00:00-05:00',1),
           ('2018-01-01T00:00:00-05:00',2), ('2017-12-31T21:00:00-05:00',3),
           ('2017-12-31T20:00:00-05:00',4), ('2017-12-31T02:00:00-05:00',5),
           ('2017-12-31T01:00:00-05:00',6), ('2017-12-30T18:00:00-05:00',7),
           ('2017-12-30T20:00:00-05:00',-1),("2017-10-12T11:00:00-04:00",-1)]
    
    # Perform the tests
    for key in keys:
        sky = report[key[0]]['sky']
        for pos in range(len(minimums)):
            expt = key[1] != -1 and key[1] <= pos
            test = violations.bad_ceiling(sky,minimums[pos])
            data = (fcn,repr(sky),repr(minimums[pos]),repr(test),repr(expt))
            assert_equals(expt, test,'%s(%s,%s) returned %s, but should have returned %s' % data)
    
    print('  %s passed all tests' % fcn)


def test_get_weather_report():
    """
    Tests the function get_weather_report
    """
    fcn = 'violations.get_weather_report'
    
    parent = os.path.split(__file__)[0]
    fpath  = os.path.join(parent,'weather.json')
    report = utils.read_json(fpath)
    
    tests = [("2017-10-12T11:00:00-04:00","2017-10-12T11:00:00-04:00"),
             ("2017-10-12T11:30:00-04:00","2017-10-12T11:00:00-04:00"),
             ("2017-10-13T09:00:00-04:00","2017-10-13T09:00:00-04:00"),
             ("2017-10-13T09:15:00-04:00","2017-10-13T09:00:00-04:00"),
             ("2017-03-12T02:00:00-05:00","2017-03-12T02:00:00-05:00"),
             ("2017-03-12T02:45:00-05:00","2017-03-12T02:00:00-05:00"),
             ("2017-03-12T03:00:00-05:00","2017-03-12T02:00:00-05:00"),
             ("2017-12-27T08:00:00-05:00","2017-12-27T08:00:00-05:00"),
             ("2017-12-27T23:00:00-05:00","2017-12-28T00:00:00-05:00")]
    
    # Perform the tests
    for test in tests:
        expct = report[test[1]]
        stamp = utils.str_to_time(test[0])
        found = violations.get_weather_report(stamp,report)
        try:
            code = 'code='+repr(found['code'])
        except:
            code = 'no code'
        
        data  = (fcn,test[0],'weather',code,repr(expct['code']))
        assert_equals(expct, found,'%s(%s,%s) returned a report with %s, not code=%s' % data)
    
    print('  %s passed all tests' % fcn)


def test_get_weather_violation():
    """
    Tests the function get_weather_violation
    """
    fcn = 'violations.get_weather_violation'
    
    parent = os.path.split(__file__)[0]
    fpath  = os.path.join(parent,'weather.json')
    report = utils.read_json(fpath)
    
    minimums = [[500,0.75,30,20],[500,1,25,15],[1000,2,25,15],
                [1500,3,30,20],[1500,5,20,10],[1500,5,25,15],
                [2000,5,20,8],[2000,8,25,15],[2000,5,30,20],
                [2500,10,25,15],[3000,10,20,8],[3000,10,20,10],
                [3500,10,20,8],[5000,10,20,10]]
    
    tests = [
        ('2017-05-14T19:00:00-04:00','','Winds','Winds','','Weather','Weather','Weather',
            'Weather','Visibility','Weather','Weather','Weather','Weather','Weather'),
        ('2017-10-12T00:00:00-04:00','','','','','','','Winds','','','Visibility',
            'Weather','Visibility','Weather','Visibility'),
        ('2017-10-29T00:00:00-04:00','Ceiling','Weather','Weather','Weather','Weather',
            'Weather','Weather','Weather','Weather','Weather','Weather','Weather',
            'Weather','Weather'),
        ('2017-11-07T13:00:00-05:00','','','','','','','Winds','Visibility','','Visibility',
            'Weather','Visibility','Weather','Weather'),
        ('2017-12-04T08:00:00-05:00','Weather','Weather','Weather','Weather','Weather',
            'Weather','Weather','Weather','Weather','Weather','Weather','Weather',
            'Weather','Weather'),
        ('2017-12-12T14:00:00-05:00','','','','Ceiling','Weather','Ceiling','Weather','Ceiling',
            'Ceiling','Ceiling','Weather','Weather','Weather','Weather'),
        ('2017-12-13T04:00:00-05:00','','','','','Weather','Visibility','Weather','Visibility',
            'Visibility','Weather','Weather','Weather','Weather','Weather'),
        ('2017-12-23T22:00:00-05:00','Ceiling','Ceiling','Ceiling','Ceiling','Weather',
            'Weather','Weather','Weather','Weather','Weather','Weather','Weather',
            'Weather','Weather'),
        ('2017-12-27T10:00:00-05:00','','','','','','','','','','','','','',''),
        ('2017-12-28T23:00:00-05:00','','','Ceiling','Ceiling','Ceiling','Ceiling',
            'Ceiling','Weather','Ceiling','Weather','Weather','Weather','Weather',
            'Weather'),
        ('2017-12-30T02:00:00-05:00','','','','','','','','','','Visibility',
            'Visibility','Visibility','Visibility','Weather'),
        ('2017-12-30T09:00:00-05:00','','Visibility','Visibility','Visibility',
            'Visibility','Visibility','Visibility','Visibility','Visibility','Visibility',
            'Visibility','Visibility','Visibility','Weather'),
        ('2017-12-30T11:00:00-05:00','','','','','','','','Visibility','','Visibility',
            'Visibility','Visibility','Visibility','Weather'),
        ('2017-12-30T12:00:00-05:00','','','','','','','','','','',
            'Ceiling','Ceiling','Ceiling','Ceiling'),
        ('2017-12-30T13:00:00-05:00','','','','','','','','','','','','','Ceiling','Ceiling'),
        ('2017-12-31T16:00:00-05:00','','','','','','','Winds','','','Weather','Weather',
            'Weather','Weather','Weather'),
        ('2017-12-31T20:00:00-05:00','','','','','','','Winds','','','Ceiling',
            'Weather','Ceiling','Weather','Ceiling'),
        ('2015-01-01T00:00:00-05:00','Unknown','Unknown','Unknown','Unknown','Unknown',
            'Unknown','Unknown','Unknown','Unknown','Unknown','Unknown','Unknown',
            'Unknown','Unknown'),
        ('2017-11-10T02:00:00-05:00','Winds','Winds','Winds','Winds','Winds','Winds',
            'Winds','Winds','Winds','Winds','Winds','Winds','Winds','Winds'),
        ('2017-04-27T06:00:00-04:00','','','','','','','','','','','','','','')]
    
    # Perform the tests
    for test in tests:
        for pos in range(len(minimums)):
            expct = test[pos+1]
            read  = report[test[0]] if test[0] in report else None
            check = violations.get_weather_violation(read,minimums[pos])
            
            data  = (fcn,repr(read),repr(minimums[pos]),repr(check),repr(expct))
            assert_equals(expct, check,'%s(%s,%s) returned %s, not %s' % data)
    
    print('  %s passed all tests' % fcn)


def test_list_weather_violations():
    """
    Tests the function list_weather_violations
    """
    fcn = 'violations.list_weather_violations'
    
    parent = os.path.split(__file__)[0]
    results = violations.list_weather_violations(parent)
    
    fpath  = os.path.join(parent,'badweather.csv')
    correct = utils.read_csv(fpath)[1:]
    
    fpath  = os.path.join(parent,'students.csv')
    students = utils.read_csv(fpath)[1:]
    
    # Hash for better comparison
    data = {}
    for item in results:
        if len(item) != len(correct[0]):
            quit_with_error('%s is not a (1-dimensional) list with %d elements.' % (item,len(correct[0])))
        data[item[0]+item[3]] = item
    results = data
    
    data = {}
    for item in correct:
        data[item[0]+item[3]] = item
    correct = data
    
    for key in correct:
        if not key in results:
            data = (fcn,correct[key][3],correct[key][0])
            quit_with_error('%s(tests) is missing the flight %s for pilot %s' % data)
    
    for key in results:
        if not key in correct:
            data = (fcn,results[key][3],results[key][0])
            message = '%s(tests) identified flight %s for pilot %s, even though it is okay' % data
            message += '\n'+flight_type(results[key],students)
            quit_with_error(message)
    
    for key in correct:
        if correct[key][-1] != results[key][-1]:
            data = (fcn,correct[key][3],correct[key][0],repr(results[key][-1]),repr(correct[key][-1]))
            message = '%s(tests) identified flight %s for pilot %s as %s, not %s.' % data
            message += '\n'+flight_type(results[key],students)
            quit_with_error(message)
    
    print('  %s passed all tests' % fcn)


def test():
    """
    Performs all tests on the module violations.
    """
    print('Testing module violations')
    test_bad_visibility()
    test_bad_winds()
    test_bad_ceiling()
    test_get_weather_report()
    test_get_weather_violation()
    test_list_weather_violations()
