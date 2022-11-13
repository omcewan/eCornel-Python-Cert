# See: https://stackoverflow.com/questions/14132789/relative-imports-for-the-billionth-time
if __package__ is None or __package__ == '':
    # Access the module if run from __main__.py (Script visibility)
    from support import *
else:
    # Access the module if run from __init__.py (Packages visibility)
    from .support import *


# Load the utils modle
utils  = load_from_path('utils')
endorsements = load_from_path('endorsements')
pilots = load_from_path('pilots')


def test_teaches_multiengine():
    """
    Tests the function teaches_multiengine
    """
    fcn = 'endorsements.teaches_multiengine'
    
    # Access the file relative to this one, not the user's terminal
    parent = os.path.split(__file__)[0]
    fpath  = os.path.join(parent,'instructors.csv')
    table = utils.read_csv(fpath)
    
    # Relevant instructors
    teachers = { 'I003', 'I010', 'I096'}
    
    for row in table[1:]:
        expct =  row[0] in teachers
        answr = endorsements.teaches_multiengine(row)
        data = (fcn,repr(row),repr(answr),repr(expct))
        assert_equals(expct,answr,'%s(%s) returned %s, not %s' % data)
    
    print('  %s passed all tests' % fcn)


def test_teaches_instrument():
    """
    Tests the function teaches_instrument
    """
    fcn = 'endorsements.teaches_instrument'
    
    # Access the file relative to this one, not the user's terminal
    parent = os.path.split(__file__)[0]
    fpath  = os.path.join(parent,'instructors.csv')
    table = utils.read_csv(fpath)
    
    # Relevant instructors
    teachers = { 'I003', 'I010', 'I032', 'I077', 'I097', 'I060'}
    
    for row in table[1:]:
        expct =  row[0] in teachers
        answr = endorsements.teaches_instrument(row)
        data = (fcn,repr(row),repr(answr),repr(expct))
        assert_equals(expct,answr,'%s(%s) returned %s, not %s' % data)
    
    print('  %s passed all tests' % fcn)


def test_is_advanced():
    """
    Tests the function is_advanced
    """
    fcn = 'endorsements.is_advanced'
    
    # Access the file relative to this one, not the user's terminal
    parent = os.path.split(__file__)[0]
    fpath  = os.path.join(parent,'fleet.csv')
    table = utils.read_csv(fpath)
    
    # Relevant planes
    planes = { '446BU', '385AT', '249SM', '625LT', '436MK'}
    
    for row in table[1:]:
        expct =  row[0] in planes
        answr = endorsements.is_advanced(row)
        data = (fcn,repr(row),repr(answr),repr(expct))
        assert_equals(expct,answr,'%s(%s) returned %s, not %s' % data)
    
    print('  %s passed all tests' % fcn)


def test_is_multiengine():
    """
    Tests the function is_multiengine
    """
    fcn = 'endorsements.is_multiengine'
    
    # Access the file relative to this one, not the user's terminal
    parent = os.path.split(__file__)[0]
    fpath  = os.path.join(parent,'fleet.csv')
    table = utils.read_csv(fpath)
    
    # Relevant planes
    planes = {'625LT'}
    
    for row in table[1:]:
        expct =  row[0] in planes
        answr = endorsements.is_multiengine(row)
        data = (fcn,repr(row),repr(answr),repr(expct))
        assert_equals(expct,answr,'%s(%s) returned %s, not %s' % data)
    
    print('  %s passed all tests' % fcn)


def test_is_ifr_capable():
    """
    Tests the function is_ifr_capable
    """
    fcn = 'endorsements.is_ifr_capable'
    
    # Access the file relative to this one, not the user's terminal
    parent = os.path.split(__file__)[0]
    fpath  = os.path.join(parent,'fleet.csv')
    table = utils.read_csv(fpath)
    
    # Relevant planes
    planes = { '684TM', '254SE', '157ZA', '548QR', '217PQ', '446BU', '385AT', 
               '249SM', '625LT', '436MK'}
    
    for row in table[1:]:
        expct =  row[0] in planes
        answr = endorsements.is_ifr_capable(row)
        data = (fcn,repr(row),repr(answr),repr(expct))
        assert_equals(expct,answr,'%s(%s) returned %s, not %s' % data)
    
    print('  %s passed all tests' % fcn)


def test_bad_endorsement():
    """
    Tests the function bad_endorsement
    """
    fcn = 'endorsements.bad_endorsement'
    
    # Access the file relative to this one, not the user's terminal
    parent = os.path.split(__file__)[0]
    
    fpath  = os.path.join(parent,'fleet.csv')
    planes = utils.read_csv(fpath)
    data = {}
    for item in planes:
        data[item[0]] = item
    planes = data
    
    fpath  = os.path.join(parent,'instructors.csv')
    teachers = utils.read_csv(fpath)
    data = {}
    for item in teachers:
        data[item[0]] = item
    teachers = data
    
    fpath  = os.path.join(parent,'students.csv')
    students = utils.read_csv(fpath)
    data = {}
    for item in students:
        data[item[0]] = item
    students = data
    
    tests = [('S00526','446BU',None,'2017-01-16T08:00:00-05:00',True),
             ('S00526','133CZ',None,'2017-01-16T08:00:00-05:00',False),
             ('S00591','446BU',None,'2017-01-23T09:00:00-05:00',True),
             ('S00536','446BU',None,'2016-12-05T12:00:00-05:00',True),
             ('S00536','446BU','I003','2016-12-05T12:00:00-05:00',False),
             ('S00536','446BU',None,'2016-12-12T09:00:00-05:00',False),
             ('S00591','446BU','I032','2017-01-23T09:00:00-05:00',False),
             ('S00847','385AT',None,'2017-08-09T12:00:00-04:00',True),
             ('S00378','625LT',None,'2017-09-26T12:00:00-04:00',True),
             ('S00378','625LT','I032','2017-09-26T12:00:00-04:00',True),
             ('S00378','625LT','I003','2017-09-26T12:00:00-04:00',False),
             ('S00378','625LT',None,'2017-09-30T12:00:00-04:00',False)]
    
    for test in tests:
        expct = test[-1]
        teach = None if test[2] is None else teachers[test[2]]
        stud  = students[test[0]]
        plan  = planes[test[1]]
        time  = utils.str_to_time(test[3])
        answr = endorsements.bad_endorsement(time,stud,teach,plan)
        data = (fcn,test[3],test[0],test[1],'None' if test[2] is None else test[2],repr(answr),repr(expct))
        assert_equals(expct,answr,'%s(%s,%s,%s,%s) returned %s, not %s' % data)
    
    print('  %s passed all tests' % fcn)


def test_bad_ifr():
    """
    Tests the function bad_ifr
    """
    fcn = 'endorsements.bad_ifr'
    
    # Access the file relative to this one, not the user's terminal
    parent = os.path.split(__file__)[0]
    
    fpath  = os.path.join(parent,'fleet.csv')
    planes = utils.read_csv(fpath)
    data = {}
    for item in planes:
        data[item[0]] = item
    planes = data
    
    fpath  = os.path.join(parent,'instructors.csv')
    teachers = utils.read_csv(fpath)
    data = {}
    for item in teachers:
        data[item[0]] = item
    teachers = data
    
    fpath  = os.path.join(parent,'students.csv')
    students = utils.read_csv(fpath)
    data = {}
    for item in students:
        data[item[0]] = item
    students = data
    
    tests = [('S00811','811AX','I077','2017-01-07T10:00:00-05:00',True),
             ('S00811','157ZA','I072','2017-01-07T10:00:00-05:00',True),
             ('S00811','157ZA','I077','2017-01-07T10:00:00-05:00',False),
             ('S00850','426JQ','I032','2017-01-17T14:00:00-05:00',True),
             ('S00789','548QR','I032','2017-08-01T14:00:00-05:00',False),
             ('S00789','811AX','I032','2017-08-01T14:00:00-05:00',True),
             ('S00789','548QR',None,'2017-08-02T14:00:00-05:00',True),
             ('S00789','811AX',None,'2017-08-03T14:00:00-05:00',True),
             ('S00789','548QR',None,'2017-08-03T14:00:00-05:00',False)]
    
    for test in tests:
        expct = test[-1]
        teach = None if test[2] is None else teachers[test[2]]
        stud  = students[test[0]]
        plan  = planes[test[1]]
        time  = utils.str_to_time(test[3])
        answr = endorsements.bad_ifr(time,stud,teach,plan)
        data = (fcn,test[3],test[0],test[1],'None' if test[2] is None else test[2],repr(answr),repr(expct))
        assert_equals(expct,answr,'%s(%s,%s,%s,%s) returned %s, not %s' % data)
    
    print('  %s passed all tests' % fcn)


def test_list_endorsement_violations():
    """
    Tests the function list_endorsement_violations
    """
    fcn = 'endorsements.list_endorsement_violations'
    
    parent = os.path.split(__file__)[0]
    results = endorsements.list_endorsement_violations(parent)
    
    fpath  = os.path.join(parent,'badpilots.csv')
    correct = utils.read_csv(fpath)[1:]
    
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
            message = ('%s(tests) identified flight %s for pilot %s, even though it is okay' % data)
            if results[key][-1].upper() == 'IFR' and results[key][5] == 'VFR':
                message += '\nThis is a VFR flight and cannot have an IFR violation.'
            quit_with_error(message)
    
    for key in correct:
        if correct[key][-1] != results[key][-1]:
            data = (fcn,correct[key][3],correct[key][0],repr(results[key][-1]),repr(correct[key][-1]))
            message = "%s('tests')  identified flight %s for pilot %s as %s, not %s" % data
            if results[key][-1] in ['IFR', 'Credentials'] and results[key][5] == 'VFR':
                message += '\nThis is a VFR flight and cannot have an IFR violation.'
            quit_with_error(message)
    
    print('  %s passed all tests' % fcn)


def test():
    """
    Performs all tests on the module endorsements.
    """
    print('Testing module endorsements')
    test_teaches_multiengine()
    test_teaches_instrument()
    test_is_advanced()
    test_is_multiengine()
    test_is_ifr_capable()
    test_bad_endorsement()
    test_bad_ifr()
    test_list_endorsement_violations()
