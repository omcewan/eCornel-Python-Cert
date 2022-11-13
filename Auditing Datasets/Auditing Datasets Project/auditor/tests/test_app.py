import os, os.path

# See: https://stackoverflow.com/questions/14132789/relative-imports-for-the-billionth-time
if __package__ is None or __package__ == '':
    # Access the module if run from __main__.py (Script visibility)
    from support import *
else:
    # Access the module if run from __init__.py (Packages visibility)
    from .support import *

# Load the utils modle
utils = load_from_path('utils')
app = load_from_path('app')

TEST_BASIC_APP   = 0
TEST_EXTENSION_1 = 1
TEST_EXTENSION_2 = 2


def test_discover_violations(level=TEST_BASIC_APP):
    fcn = 'app.discover_violations'
    file = 'scratch.csv'
    printer = Printer()
    app.print = printer.print
    
    parent = os.path.split(__file__)[0]
    output = os.path.join(parent,file)
    if os.path.exists(output):
        os.remove(output)
    
    correct = [93,125,144]
    expect = '%s violations found.' % str(correct[level])
    results = app.discover_violations(parent,None)
    if not printer.printed:
        quit_with_error("%s('tests',%s) did not print the number of violations found" % (fcn,repr(file)))
    elif len(printer.printed) > 1:
        quit_with_error("%s('tests',%s) printed more than one line"  % (fcn,repr(file)))
    elif printer.printed[0].strip() == expect[:-1]:
        quit_with_error("%s('tests',%s) is missing a period from its printed output"  % (fcn,repr(file)))
    elif printer.printed[0].strip() != expect:
        data = (fcn,repr(file),repr(printer.printed[0].strip()),repr(expect))
        quit_with_error("%s('tests',%s) printed %s, not %s"  % data)
    printer.reset()
    
    results = app.discover_violations(parent,output)
    if not printer.printed:
        quit_with_error("%s('tests',%s) did not print the number of violations found" % (fcn,repr(file)))
    elif len(printer.printed) > 1:
        quit_with_error("%s('tests',%s) printed more than one line"  % (fcn,repr(file)))
    elif printer.printed[0].strip() == expect[:-1]:
        quit_with_error("%s('tests',%s) is missing a period from its printed output"  % (fcn,repr(file)))
    elif printer.printed[0].strip() != expect:
        data = (fcn,repr(file),repr(printer.printed[0].strip()),repr(expect))
        quit_with_error("%s('tests',%s) printed %s, not %s"  % data)
    printer.reset()
    
    if not os.path.exists(output):
        quit_with_error("%s('tests',%s) did not create the file %s" % (fcn,repr(file),repr(file)))
    
    try:
        data = utils.read_csv(output)
    except:
        quit_with_error("The file %s could not be read. Make sure it has the right format." % repr(output))
    
    if len(data) == 0:
        quit_with_error("The file %s is empty" % repr(output))
    
    header1 = ['STUDENT','AIRPLANE','INSTRUCTOR','TAKEOFF','LANDING','FILED','AREA','REASON']
    header2 = list(map(lambda x: x.upper(),data[0]))
    assert_equals(header1,header2,'The header for %s is %s, not %s' % (repr(output),header1,header2))
    
    # Hash the student answers for comparison
    found = {}
    for item in data[1:]:
        found[item[0]+item[3]] = item
    
    fpath  = os.path.join(parent,'badweather.csv')
    weather = utils.read_csv(fpath)[1:]
    data = {}
    for item in weather:
        data[item[0]+item[3]] = item
    weather = data
    
    fpath  = os.path.join(parent,'badpilots.csv')
    pilots = utils.read_csv(fpath)[1:]
    data = {}
    for item in pilots:
        data[item[0]+item[3]] = item
    pilots = data
    
    fpath  = os.path.join(parent,'badplanes.csv')
    planes = utils.read_csv(fpath)[1:]
    data = {}
    for item in planes:
        data[item[0]+item[3]] = item
    planes = data
    
    for key in weather:
        if not key in found:
            data = (repr(output),weather[key][3],weather[key][0])
            quit_with_error('File %s is missing the bad weather flight %s for pilot %s' % data)
    if level >= TEST_EXTENSION_1:
        for key in pilots:
            if not key in found:
                data = (repr(output),pilots[key][3],pilots[key][0])
                quit_with_error('File %s is missing the bad endorsement flight %s for pilot %s' % data)
    if level >= TEST_EXTENSION_2:
        for key in planes:
            if not key in found:
                data = (repr(output),planes[key][3],planes[key][0])
                quit_with_error('File %s is missing the bad inspection flight %s for pilot %s' % data)
    
    for key in found:
        match = key in weather
        if level >= TEST_EXTENSION_1:
            match = match or key in pilots
        if level >= TEST_EXTENSION_2:
            match = match or key in planes
        if not match:
            data = (repr(output),found[key][3],found[key][0])
            quit_with_error('File %s identified flight %s for pilot %s, even though it is okay' % data)
    
    for key in found:
        reason2 = found[key][-1]
        reason1 = None
        if key in weather:
            reason1 = weather[key][-1]
        if level >= TEST_EXTENSION_1 and key in pilots:
            reason1 = pilots[key][-1]
        if level >= TEST_EXTENSION_2 and key in planes:
            reason1 = planes[key][-1]
        data = (repr(output),found[key][3],found[key][0],repr(reason1),repr(reason2))
        assert_equals(reason1,reason2,
                     "File %s identified flight %s for pilot %s as %s, not %s" % data)
    
    app.print = print
    print('  %s passed all tests' % fcn)


def check_execute_error(lines,value):
    correct = 'Usage: python auditor dataset [output.csv]'
    if len(lines) == 0:
        quit_with_error('app.execute(%s) did not print out an error message' % repr(value))
    elif len(lines) > 1:
        quit_with_error('app.execute(%s) printed more than one line. \n\nOutput:\n\n%s' % (repr(value), "\n".join(lines)))
    elif lines[0] != correct:
        quit_with_error('app.execute(%s) did not print the error message %s' % (repr(value),repr(correct)))


def test_execute():
    fcn = 'app.execute'
    
    import types
    
    # Capture the helper functions
    printer = Printer()
    app.discover_violations = lambda x,y: (printer.print(x),printer.print(y))
    app.tests = types.ModuleType('tests')
    app.tests.test_all = lambda : printer.print('True')
    app.tests.test_app = lambda : printer.print('False')
    app.tests.test_utils = lambda : printer.print('False')
    app.tests.test_pilots = lambda : printer.print('False')
    app.tests.test_violations = lambda : printer.print('False')
    app.tests.test_endorsements = lambda : printer.print('False')
    app.tests.test_inspections = lambda : printer.print('False')
    app.print = printer.print
    
    correct = 'Usage: python auditor dataset [output.csv]'
    
    value = []
    app.execute(value)
    check_execute_error(printer.printed,value)
    printer.reset()
    
    value = ['KITH-2017','--test']
    app.execute(value)
    check_execute_error(printer.printed,value)
    printer.reset()
    
    value = ['--test','KITH-2017']
    app.execute(value)
    check_execute_error(printer.printed,value)
    printer.reset()
    
    value = ['KITH-2017','output.csv','--test']
    app.execute(value)
    check_execute_error(printer.printed,value)
    printer.reset()
    
    value = ['KITH-2017','--test','output.csv']
    app.execute(value)
    check_execute_error(printer.printed,value)
    printer.reset()
    
    value = ['--test','KITH-2017','output.csv']
    app.execute(value)
    check_execute_error(printer.printed,value)
    printer.reset()
    
    value = ['KITH-2017','output.csv','extra.csv']
    app.execute(value)
    check_execute_error(printer.printed,value)
    printer.reset()
    
    value = ['--test']
    app.execute(value)
    if len(printer.printed) == 0:
        quit_with_error("app.execute(%s) did not call a test procedure" % repr(value))
    elif len(printer.printed) > 1:
        quit_with_error("app.execute(%s) did more than just call 'test_all'" % repr(value))
    elif printer.printed[0].strip() == 'False':
        quit_with_error("app.execute(%s) called a test procedure other than 'test_all'" % repr(value))
    elif printer.printed[0].strip() != 'True':
        quit_with_error("app.execute(%s) did not call 'test_all'" % repr(value))
    printer.reset()
    
    value = ['KITH-2017',None]
    app.execute(value)
    if len(printer.printed) in [0,1]:
        quit_with_error("app.execute(%s) did not call 'discover_violations'" % repr(value))
    elif len(printer.printed) > 2:
        quit_with_error("app.execute(%s) did more than just call 'discover_violations'" % repr(value))
    elif printer.printed[0].strip() != str(value[0]):
        quit_with_error("app.execute(%s) did not call 'discover_violations'" % repr(value))
    elif printer.printed[1].strip() != str(value[1]):
        quit_with_error("app.execute(%s) did not call 'discover_violations'" % repr(value))
    printer.reset()
    
    value = ['KITH-2017','output.csv']
    app.execute(value)
    if len(printer.printed) in [0,1]:
        quit_with_error("app.execute(%s) did not call 'discover_violations'" % repr(value))
    elif len(printer.printed) > 2:
        quit_with_error("app.execute(%s) did more than just call 'discover_violations'" % repr(value))
    elif printer.printed[0].strip() != str(value[0]):
        quit_with_error("app.execute(%s) did not call 'discover_violations'" % repr(value))
    elif printer.printed[1].strip() != str(value[1]):
        quit_with_error("app.execute(%s) did not call 'discover_violations'" % repr(value))
    printer.reset()
    
    print('  %s passed all tests' % fcn)


def test(level=TEST_BASIC_APP):
    """
    Performs all tests on the module app.
    """
    print('Testing module app (this may take a while)')
    test_discover_violations(level)
    test_execute()
