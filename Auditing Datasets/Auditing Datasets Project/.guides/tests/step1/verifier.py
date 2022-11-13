"""
The verification functions for Course 6 scripts

This file is insecurely available to students, but if they find it and modify it, they
really did not need this course.

Author: Walker M. White
Date:   November 19, 2019
"""
import os, os.path, sys
import importlib, importlib.util
import traceback
import inspect
import builtins
import ast
import json
from modlib import load_from_path, Environment

# For support
import introcs

#mark Constants

# The status codes
TEST_SUCCESS      = 0
FAIL_NO_FILE      = 1
FAIL_BAD_STYLE    = 2
FAIL_CRASHES      = 4
FAIL_INCORRECT    = 5


WORKSPACE = [os.path.expanduser('~'),'workspace']
TESTFILES = WORKSPACE+['.guides','tests','testfiles']


# The proper contents for file1.csv
FILE1 = [['STUDENT','AIRPLANE','INSTRUCTOR','TAKEOFF','LANDING','FILED','AREA'],
['S00309','738GG','I076','2015-01-12T09:00:00-05:00','2015-01-12T11:00:00-05:00','VFR','Pattern'],
['S00308','133CZ','I053','2015-01-13T09:00:00-05:00','2015-01-13T12:00:00-05:00','VFR','Practice Area'],
['S00324','426JQ','I053','2015-02-04T11:00:00-05:00','2015-02-04T14:00:00-05:00','VFR','Cross Country'],
['S00319','811AX','I072','2015-02-06T13:00:00-05:00','2015-02-06T15:00:00-05:00','VFR','Pattern'],
['S00321','738GG','I072','2015-02-08T10:00:00-05:00','2015-02-08T13:00:00-05:00','VFR','Practice Area'],
['S00308','811AX','I072','2015-02-23T09:00:00-05:00','2015-02-23T13:00:00-05:00','VFR','Cross Country']]


# The proper contents for file2.csv
FILE2 = [['TAIL NO','TYPE','CAPABILITY','ADVANCED','MULTIENGINE','ANNUAL','HOURS'],
['133CZ','Cessna 152','VFR','No','No','2016-04-15','88'],
['811AX','Cessna 152','VFR','No','No','2016-01-22','39'],
['426JQ','Cessna 152','VFR','No','No','2016-07-30','31']]


# The proper contents for file1.json
FILE3 = {
    "2018-01-01T00:00:00-05:00": {
        "visibility": {
            "prevailing": 1.75,
            "units": "SM"
        },
        "wind": {
            "speed": 13.0,
            "crosswind": 5.0,
            "units": "KT"
        },
        "temperature": {
            "value": -15.0,
            "units": "C"
        },
        "sky": [
            {
                "cover": "clouds",
                "type": "broken",
                "height": 1200.0,
                "units": "FT"
            },
            {
                "type": "overcast",
                "height": 1800.0,
                "units": "FT"
            }
        ],
        "weather": [
            "light snow",
            "mist"
        ],
        "code": "201801010456Z"
    },
    "2017-12-31T23:00:00-05:00": {
        "visibility": {
            "prevailing": 1.75,
            "units": "SM"
        },
        "wind": {
            "speed": 13.0,
            "crosswind": 5.0,
            "units": "KT"
        },
        "temperature": {
            "value": -15.0,
            "units": "C"
        },
        "sky": [
            {
                "cover": "clouds",
                "type": "broken",
                "height": 1300.0,
                "units": "FT"
            },
            {
                "type": "overcast",
                "height": 2200.0,
                "units": "FT"
            }
        ],
        "weather": [
            "light snow",
            "mist"
        ],
        "code": "201801010356Z"
    },
    "2017-12-31T22:00:00-05:00": {
        "visibility": {
            "prevailing": 3.0,
            "units": "SM"
        },
        "wind": {
            "speed": 11.0,
            "crosswind": 7.0,
            "units": "KT"
        },
        "temperature": {
            "value": -15.0,
            "units": "C"
        },
        "sky": [
            {
                "type": "overcast",
                "height": 1300.0,
                "units": "FT"
            }
        ],
        "weather": [
            "light snow",
            "mist"
        ],
        "code": "201801010317Z"
    },
    "2017-12-31T21:00:00-05:00": {
        "visibility": {
            "prevailing": 10.0,
            "units": "SM"
        },
        "wind": {
            "speed": 10.0,
            "crosswind": 7.0,
            "units": "KT"
        },
        "temperature": {
            "value": -16.1,
            "units": "C"
        },
        "sky": [
            {
                "type": "overcast",
                "height": 1700.0,
                "units": "FT"
            }
        ],
        "code": "201801010156Z"
    }
}


# The proper contents for file2.json
FILE4 = [
    {
        "cover": "clouds",
        "type": "broken",
        "height": 1200.0,
        "units": "FT"
    },
    {
        "type": "overcast",
        "height": 1800.0,
        "units": "FT"
    }
]

# A longer version of FILE1 to test for proper handling of rows and columns
FILE5 = [['STUDENT','AIRPLANE','INSTRUCTOR','TAKEOFF','LANDING','FILED','AREA'],
['S00309','738GG','I076','2015-01-12T09:00:00-05:00','2015-01-12T11:00:00-05:00','VFR','Pattern'],
['S00308','133CZ','I053','2015-01-13T09:00:00-05:00','2015-01-13T12:00:00-05:00','VFR','Practice Area'],
['S00324','426JQ','I053','2015-02-04T11:00:00-05:00','2015-02-04T14:00:00-05:00','VFR','Cross Country'],
['S00319','811AX','I072','2015-02-06T13:00:00-05:00','2015-02-06T15:00:00-05:00','VFR','Pattern'],
['S00321','738GG','I072','2015-02-08T10:00:00-05:00','2015-02-08T13:00:00-05:00','VFR','Practice Area'],
['S00308','811AX','I072','2015-02-23T09:00:00-05:00','2015-02-23T13:00:00-05:00','VFR','Cross Country'],
['S00810','157ZA','I061','2017-01-02T09:00:00-05:00','2017-01-02T11:00:00-05:00','VFR','Pattern'],
['S00843','217PQ','I076','2017-01-02T09:00:00-05:00','2017-01-02T11:00:00-05:00','VFR','Pattern']]

#mark -
#mark Helpers
def parse_file(name):
    """
    Returns an AST of the file, or a error message if it cannot be parsed.
    
    Parameter name: The file name
    Precondition: name is a string
    """
    import ast
    path = os.path.join(*WORKSPACE,name)
    try:
        with open(path) as file:
            result = ast.parse(file.read())
        return result
    except Exception as e:
        msg = traceback.format_exc(0)
        msg = msg.replace('<unknown>',name)
        return msg

def import_module(package,name,step=0):
    """
    Returns a reference to the module.
    
    Returns an error message if it fails.
    
    Parameter name: The module name
    Precondition: name is a string
    """
    try:
        import types
        refs = os.path.splitext(name)[0]
        environment = Environment(refs,WORKSPACE+[package])
        if not environment.execute():
            return '\n'.join(environment.printed)+'\n'
        return environment
    except Exception as e:
        msg = traceback.format_exc(0)
        pos2 = msg.find('^')
        pos1 = msg.rfind(')',0,pos2)
        if 'SyntaxError: unexpected EOF' in msg or 'IndentationError' in msg:
            msg = 'Remember to include and indent the docstring properly.\n'+msg
        elif pos1 != -1 and pos2 != -1 and not msg[pos1+1:pos2].strip():
            msg = 'Remember to end the header with a colon.\n'+msg
        else:
            msg = ("File %s has a major syntax error.\n" % repr(name))+msg
        return msg


# Localized error codes
def get_docstring(module):
    """
    Returns the module docstring as a list of lines
    
    If there is no docstring, this function returns None.
    
    Parameter module: The module
    Precondition: module is a ModuleType object
    """
    if module.__doc__ is None:
        return None
    
    lines = module.__doc__.split('\n')
    lines = list(map(lambda x: x.strip(),lines))
    
    start = -1
    for pos in range(len(lines)):
        if lines[pos].strip():
            start = pos
            break
    
    if start == -1:
        return []
    
    end = -1
    for pos in range(1,len(lines)-start):
        if lines[len(lines)-pos].strip():
            end = len(lines)-pos
            break
    
    if end == -1:
        return []
    
    return lines[start:end+1]


# Localized error codes
NAME_MISSING     = 1
NAME_INCOMPLETE  = 2

def check_name(text):
    """
    Returns TEST_SUCCESS if the name is correct, and error code otherwise
    
    Parameter text: The docstring text as a list.
    Precondition: text is a list of strings
    """
    if not text[-2].lower().startswith('author:'):
        return NAME_MISSING
    if not text[-2][7:].strip():
        return NAME_INCOMPLETE
    if 'your name here' in text[-2][7:].lower():
        return NAME_INCOMPLETE
    return TEST_SUCCESS


# Localized error codes
DATE_MISSING     = 1
DATE_INCOMPLETE  = 2

def check_date(text):
    """
    Returns TEST_SUCCESS if the date is correct, and error code otherwise
    
    Parameter text: The docstring text as a list.
    Precondition: text is a list of strings
    """
    if not text[-1].lower().startswith('date:'):
        return DATE_MISSING
    
    date = text[-1][5:].strip()
    try:
        import dateutil.parser as util
        temp = util.parse(date)
        return TEST_SUCCESS
    except:
        return DATE_INCOMPLETE


pass
#mark -
#mark Subgraders
def grade_docstring(package,module,step=0,outp=sys.stdout):
    """
    Returns the test result and score for the docstring.
    
    The step parameter is the phase in the grading pass.  Step 0 is a verification step
    and will stop at the first error found.  Otherwise it will continue through and try 
    to find all errors.
    
    Parameter package: The application package
    Precondition: package is a string
    
    Parameter module: The module to grade
    Precondition: module is a string
    
    Parameter step: The current verfication/grading step
    Precondition: grade is 0 or 1
    
    Parameter outp: The output stream
    Precondition: outp is a stream writer
    """
    env = import_module(package,module)
    if type(env) == str:
        outp.write(env)
        return (FAIL_CRASHES, 0)
    
    score = 1
    module = env.module
    docs = get_docstring(module)
    
    if type(docs) is None:
        outp.write('There is no module docstring in %s.\n' % repr(module))
        return (FAIL_BAD_STYLE,0)
    elif not docs:
        outp.write('The docstring for %s is empty.\n' % repr(module))
        return (FAIL_BAD_STYLE,0)
    
    test = check_name(docs)
    if test:
        if test == NAME_MISSING:
            outp.write("The second-to-last line in the module docstring does not start with 'Author:'\n")
            score -= 0.5
        if test == NAME_INCOMPLETE:
            outp.write("There is no name after 'Author:' in the module docstring.\n")
            score -= 0.4
        if not step:
            return (FAIL_BAD_STYLE,max(0,score))
    test = check_date(docs)
    if test:
        if test == DATE_MISSING:
            outp.write("The last line in the module docstring does not start with 'Date:'\n")
            score -= 0.5
        if test == DATE_INCOMPLETE:
            outp.write("The date after 'Date:' in the module docstring is invalid .\n")
            score -= 0.4
        if not step:
            return (FAIL_BAD_STYLE, max(0,score))
    
    return (TEST_SUCCESS, max(0,score))


def grade_func1(package,module,step=0,outp=sys.stdout):
    """
    Returns the test result and score for the implementation of read_csv
    
    The step parameter is the phase in the grading pass.  Step 0 is a verification step
    and will stop at the first error found.  Otherwise it will continue through and try 
    to find all errors.
    
    Parameter package: The application package
    Precondition: package is a string
    
    Parameter module: The module to grade
    Precondition: module is a string
    
    Parameter step: The current verfication/grading step
    Precondition: grade is 0 or 1
    
    Parameter outp: The output stream
    Precondition: outp is a stream writer
    """
    score = 1
    env = import_module(package,module)
    function = 'read_csv'
    
    if type(env) == str:
        outp.write(env)
        return (FAIL_CRASHES, 0)
    elif not hasattr(env.module,function):
        outp.write("File %s is missing the header for %s.\n" % (repr(module),repr(function)))
        return (FAIL_INCORRECT, 0)
    
    testcases = [('file1.csv',FILE1),('file2.csv',FILE2)]
    
    func = getattr(env.module,function)
    printed = False
    unclosed = False
    for data in testcases:
        fpath = os.path.join(*TESTFILES,data[0])
        try:
            env.reset()
            received = func(fpath)
            if received != data[1]:
                outp.write("The call %s(%s) returns %s, not %s.\n" % (function, repr(fpath), repr(received), repr(data[1])))
                score -= 1/len(testcases)
                if not step:
                    return (FAIL_INCORRECT,max(0,score))
            if len(env.printed) != 0:
                printed = True
            if len(env.files) != 0:
                unclosed = True
        except:
            import traceback
            outp.write("The call %s(%s) crashed.\n" % (function, str(fpath)))
            outp.write(traceback.format_exc()+'\n')
            score -= 1/len(testcases)
            if not step:
                return (FAIL_INCORRECT,max(0,score))
    
    if printed:
        outp.write("You must remove all debugging print statements from %s.\n" % repr(function))
        score -= 0.1
        if not step:
            return (FAIL_BAD_STYLE,max(0,score))
    
    if unclosed:
        outp.write("You forgot to close your open file in %s.\n" % repr(function))
        score -= 0.1
        if not step:
            return (FAIL_BAD_STYLE,max(0,score))
    
    return (TEST_SUCCESS,max(0,score))


def grade_func2(package,module,step=0,outp=sys.stdout):
    """
    Returns the test result and score for the implementation of read_csv
    
    The step parameter is the phase in the grading pass.  Step 0 is a verification step
    and will stop at the first error found.  Otherwise it will continue through and try 
    to find all errors.
    
    Parameter package: The application package
    Precondition: package is a string
    
    Parameter module: The module to grade
    Precondition: module is a string
    
    Parameter step: The current verfication/grading step
    Precondition: grade is 0 or 1
    
    Parameter outp: The output stream
    Precondition: outp is a stream writer
    """
    score = 1
    env = import_module(package,module)
    function = 'write_csv'
    
    if type(env) == str:
        outp.write(env)
        return (FAIL_CRASHES, 0)
    elif not hasattr(env.module,function):
        outp.write("File %s is missing the header for %s.\n" % (repr(module),repr(function)))
        return (FAIL_INCORRECT, 0)
    
    testcases = [('temp1.csv',FILE1,'file1.csv'),('temp2.csv',FILE2,'file2.csv')]
    
    func = getattr(env.module,function)
    printed = False
    unclosed = False
    for data in testcases:
        innpath = os.path.join(*TESTFILES,data[2])
        outpath = os.path.join(*TESTFILES,data[0])
        short = repr(data[1])[:10]+'...'
        try:
            env.reset()
            func(data[1],outpath)
            if not os.path.exists(outpath):
                outp.write("The call %s(%s,%s) did not create a file.\n" % (function, short, repr(outpath)))
                score -= 1/len(testcases)
                if not step:
                    return (FAIL_INCORRECT,max(0,score))
            else:
                with open(innpath) as file:
                    correct = file.read()
                with open(outpath) as file:
                    actual = file.read()
                if correct != actual:
                    outp.write("The contents of the file %s do not match %s.\n" % (repr(outpath), repr(innpath)))
                    score -= 1/len(testcases)
                    if not step:
                        return (FAIL_INCORRECT,max(0,score))
            if len(env.printed) != 0:
                printed = True
            if len(env.files) != 0:
                unclosed = True
        except:
            import traceback
            outp.write("The call %s(%s,%s) crashed.\n" % (function, short, repr(outpath)))
            outp.write(traceback.format_exc()+'\n')
            score -= 1/len(testcases)
            if not step:
                return (FAIL_INCORRECT,max(0,score))
    
    if printed:
        outp.write("You must remove all debugging print statements from %s.\n" % repr(function))
        score -= 0.1
        if not step:
            return (FAIL_BAD_STYLE,max(0,score))

    if unclosed:
        outp.write("You forgot to close your open file in %s.\n" % repr(function))
        score -= 0.1
        if not step:
            return (FAIL_BAD_STYLE,max(0,score))
    
    return (TEST_SUCCESS,max(0,score))


def grade_func3(package,module,step=0,outp=sys.stdout):
    """
    Returns the test result and score for the implementation of read_json
    
    The step parameter is the phase in the grading pass.  Step 0 is a verification step
    and will stop at the first error found.  Otherwise it will continue through and try 
    to find all errors.
    
    Parameter package: The application package
    Precondition: package is a string
    
    Parameter module: The module to grade
    Precondition: module is a string
    
    Parameter step: The current verfication/grading step
    Precondition: grade is 0 or 1
    
    Parameter outp: The output stream
    Precondition: outp is a stream writer
    """
    score = 1
    env = import_module(package,module)
    function = 'read_json'
    
    if type(env) == str:
        outp.write(env)
        return (FAIL_CRASHES, 0)
    elif not hasattr(env.module,function):
        outp.write("File %s is missing the header for %s.\n" % (repr(module),repr(function)))
        return (FAIL_INCORRECT, 0)
    
    testcases = [('file3.json',FILE3),('file4.json',FILE4)]
    func = getattr(env.module,function)
    printed = False
    unclosed = False
    for data in testcases:
        fpath = os.path.join(*TESTFILES,data[0])
        try:
            env.reset()
            received = func(fpath)
            expected = data[1]
            if type(received) != type(expected):
                outp.write("The call %s(%s) returns a value of type %s, not %s.\n" % (function, repr(fpath), repr(type(received)), repr(type(expected))))
                score -= 1/len(testcases)
                if not step:
                    return (FAIL_INCORRECT,max(0,score))
            if received != expected:
                outp.write("The call %s(%s) returns %s, not %s.\n" % (function, repr(fpath), repr(received), repr(expected)))
                score -= 1/len(testcases)
                if not step:
                    return (FAIL_INCORRECT,max(0,score))
            if len(env.printed) != 0:
                printed = True
            if len(env.files) != 0:
                unclosed = True
        except:
            import traceback
            outp.write("The call %s(%s) crashed.\n" % (function, repr(fpath)))
            outp.write(traceback.format_exc()+'\n')
            score -= 1/len(testcases)
            if not step:
                return (FAIL_INCORRECT,max(0,score))
    
    if printed:
        outp.write("You must remove all debugging print statements from %s.\n" % repr(function))
        score -= 0.1
        if not step:
            return (FAIL_BAD_STYLE,max(0,score))

    if unclosed:
        outp.write("You forgot to close your open file in %s.\n" % repr(function))
        score -= 0.1
        if not step:
            return (FAIL_BAD_STYLE,max(0,score))
    
    return (TEST_SUCCESS,max(0,score))


def grade_func4(package,module,step=0,outp=sys.stdout):
    """
    Returns the test result and score for the implementation of str_to_time
    
    The step parameter is the phase in the grading pass.  Step 0 is a verification step
    and will stop at the first error found.  Otherwise it will continue through and try 
    to find all errors.
    
    Parameter package: The application package
    Precondition: package is a string
    
    Parameter module: The module to grade
    Precondition: module is a string
    
    Parameter step: The current verfication/grading step
    Precondition: grade is 0 or 1
    
    Parameter outp: The output stream
    Precondition: outp is a stream writer
    """
    score = 1
    env = import_module(package,module)
    function = 'str_to_time'
    
    if type(env) == str:
        outp.write(env)
        return (FAIL_CRASHES, 0)
    elif not hasattr(env.module,function):
        outp.write("File %s is missing the header for %s.\n" % (repr(module),repr(function)))
        return (FAIL_INCORRECT, 0)

    # Check for try...except not present or with more than one line in the try clause STT
    tree = parse_file("auditor/%s" % module)
    # Find the str_to_time function in the tree
    afunc = next((n for n in ast.walk(tree) if type(n) == ast.FunctionDef and n.name == 'str_to_time'), None)
    if afunc:
        # Find the first try block in the function's tree
        atry = next((n for n in ast.walk(afunc) if type(n) == ast.Try), None)
        if atry:
            # Fail if more than one expression inside the try clause.
            if len(atry.body) > 1:
                outp.write("The try clause in %s should only have the line of code that calls parse. " % repr(function))
                outp.write("(Otherwise unexpected errors in other lines of code will be harder to identify.)\n")
                score -= 0.5
                if not step:
                    return (FAIL_INCORRECT,max(0,score))
            else:
                # Error if parse is not called in the try clause
                call = next((n for n in ast.walk(atry) if type(n) == ast.Call), None)
                if call:
                    funcname = call.func.id if type(call.func) == ast.Name else call.func.attr
                    if funcname != 'parse':
                        outp.write("Unable to find where 'parse' is called inside the try clause in %s.\n" % repr(function))
                        score -= 0.5
                        if not step:
                            return (FAIL_INCORRECT,max(0,score))
                else:
                    outp.write("There are no calls to parse inside the try clause in %s.\n" % repr(function))
                    score -= 0.5
                    if not step:
                        return (FAIL_INCORRECT,max(0,score))
        else:
            outp.write("You do not have a try clause in your implementation of %s.\n" % repr(function))
            score -= 0.5
            if not step:
                return (FAIL_INCORRECT,max(0,score))

    from datetime import datetime
    import pytz
    offset = datetime(2016,5,12,16,23)
    ast0 = pytz.timezone('America/Puerto_Rico')
    est = pytz.timezone('EST')
    eastern  = pytz.timezone('US/Eastern')
    central  = pytz.timezone('America/Chicago')
    offset = est.localize(offset)
    today = datetime.now()
    testcases = [('2016-04-15',                 None,               datetime(2016,4,15)),
                 ('October 12, 2019',           None,               datetime(2019,10,12)),
                 ('Octover 12, 2019',           None,               None),
                 ('2016-04-15T10:15:45',        None,               datetime(2016,4,15,10,15,45)),
                 ('2017-08-02 13:00:15',        None,               datetime(2017,8,2,13,0,15)),
                 ('10:15 pm, October 12, 2019', None,               datetime(2019,10,12,22,15)),
                 ('22:15 pm, October 12, 2019', None,               None),
                 ('2016-05-12',                 None,               datetime(2016,5,12)),
                 ('16:23',                      None,               datetime(today.year,today.month,today.day,16,23)),
                 ('16:23-5:00',                 None,               est.localize(datetime(today.year,today.month,today.day,16,23))),
                 ('2016-05-12T16:23-5:00',      None,               est.localize(datetime(2016,5,12,16,23))),
                 ('2016-05-12T16:23',           offset,             est.localize(datetime(2016,5,12,16,23))),
                 ('2016-05-12T16:23-4:00',      offset,             ast0.localize(datetime(2016,5,12,16,23))),
                 ('2016-05-12T16:23',           'America/Chicago',  central.localize(datetime(2016,5,12,16,23))),
                 ('2016-05-12T16:23',           'US/Eastern',       eastern.localize(datetime(2016,5,12,16,23))),
                 ('2016-05-12T16:23-5:00',      'US/Eastern',       central.localize(datetime(2016,5,12,16,23)))]
    func = getattr(env.module,function)
    printed = False
    for data in testcases:
        try:
            env.reset()
            received = func(*data[:2])
            expected = data[2]
            if not received is None and type(received) != datetime:
                outp.write("The call %s%s does not return a datetime object.\n" % (function, repr(data[:2])))
                score -= 1/len(testcases)
                if not step:
                    return (FAIL_INCORRECT,max(0,score))
            if received != expected:
                outp.write("The call %s%s returns %s, not %s.\n" % (function, repr(data[:2]), repr(received), repr(expected)))
                score -= 1/len(testcases)
                if not step:
                    return (FAIL_INCORRECT,max(0,score))
            if len(env.printed) != 0:
                printed = True
        except:
            import traceback
            outp.write("The call %s%s crashed.\n" % (function, repr(data[:2])))
            outp.write(traceback.format_exc()+'\n')
            score -= 1/len(testcases)
            if not step:
                return (FAIL_INCORRECT,max(0,score))
    
    if printed:
        outp.write("You must remove all debugging print statements from %s.\n" % repr(function))
        score -= 0.1
        if not step:
            return (FAIL_BAD_STYLE,max(0,score))
    
    return (TEST_SUCCESS,max(0,score))


def grade_func5(package,module,step=0,outp=sys.stdout):
    """
    Returns the test result and score for the implementation of daytime
    
    The step parameter is the phase in the grading pass.  Step 0 is a verification step
    and will stop at the first error found.  Otherwise it will continue through and try 
    to find all errors.
    
    Parameter package: The application package
    Precondition: package is a string
    
    Parameter module: The module to grade
    Precondition: module is a string
    
    Parameter step: The current verfication/grading step
    Precondition: grade is 0 or 1
    
    Parameter outp: The output stream
    Precondition: outp is a stream writer
    """
    score = 1
    env = import_module(package,module)
    function = 'daytime'
    
    if type(env) == str:
        outp.write(env)
        return (FAIL_CRASHES, 0)
    elif not hasattr(env.module,function):
        outp.write("File %s is missing the header for %s.\n" % (repr(module),repr(function)))
        return (FAIL_INCORRECT, 0)
    
    filepath = os.path.join(*TESTFILES,'daycycle.json')
    file = open(filepath)
    daycycle = json.loads(file  .read())
    file.close()
    
    from datetime import datetime
    import pytz
    testcases = [(datetime(2015,6,5,7),True,True),    (datetime(2015,6,5,17),True,True),
                 (datetime(2015,10,31,6),False,True), (datetime(2015,10,31,17),True,False),
                 (datetime(2015,11,17,7),True,True),  (datetime(2015,11,17,17),False,False),
                 (datetime(2015,12,11,7),False,True), (datetime(2015,12,11,17),False,False),
                 (datetime(2016,11,1,7),True,True),   (datetime(2016,11,1,17),False,False),
                 (datetime(2017,11,17,7),False,True), (datetime(2017,11,17,17),False,False),
                 (datetime(2018,6,5,6),True,True),    (datetime(2018,6,5,19),True,False),
                 (datetime(2018,11,15,7),True,True),  (datetime(2018,11,15,17),False,False),
                 (datetime(2018,11,15,6),False,True), (datetime(2018,11,15,16),True,False)]
    eastern = pytz.timezone('US/Eastern')
    central = pytz.timezone('America/Chicago')
    func = getattr(env.module,function)
    printed = False
    for data in testcases:
        try:
            env.reset()
            input = eastern.localize(data[0])
            received = func(input,daycycle)
            expected = data[1]
            if received != expected:
                outp.write("The call %s(%s,%s) returns %s, not %s.\n" % (function, repr(input), 'daycycle', repr(received), repr(expected)))
                score -= 0.5/len(testcases)
                if not step:
                    return (FAIL_INCORRECT,max(0,score))
            if len(env.printed) != 0:
                printed = True
        except:
            import traceback
            outp.write("The call %s(%s,%s) crashed.\n" % (function, repr(input), 'daycycle'))
            outp.write(traceback.format_exc()+'\n')
            score -= 0.5/len(testcases)
            if not step:
                return (FAIL_INCORRECT,max(0,score))
        try:
            env.reset()
            input = central.localize(data[0])
            received = func(input,daycycle)
            expected = data[2]
            if received != expected:
                outp.write("The call %s(%s,%s) returns %s, not %s.\n" % (function, repr(input), 'daycycle', repr(received), repr(expected)))
                score -= 0.5/len(testcases)
                if not step:
                    return (FAIL_INCORRECT,max(0,score))
            if len(env.printed) != 0:
                printed = True
        except:
            import traceback
            outp.write("The call %s(%s,%s) crashed.\n" % (function, repr(input), 'daycycle'))
            outp.write(traceback.format_exc()+'\n')
            score -= 0.5/len(testcases)
            if not step:
                return (FAIL_INCORRECT,max(0,score))
        # Test the case of no time zone (Same result as first test above.) (Added by STT)
        try:
            env.reset()
            input = data[0]
            received = func(input,daycycle)
            expected = data[1]
            if received != expected:
                outp.write("The call %s(%s,%s) returns %s, not %s.\n" % (function, repr(input), 'daycycle', repr(received), repr(expected)))
                score -= 0.5/len(testcases)
                if not step:
                    return (FAIL_INCORRECT,max(0,score))
            if len(env.printed) != 0:
                printed = True
        except:
            import traceback
            outp.write("The call %s(%s,%s) crashed.\n" % (function, repr(input), 'daycycle'))
            outp.write(traceback.format_exc()+'\n')
            score -= 0.5/len(testcases)
            if not step:
                return (FAIL_INCORRECT,max(0,score))
    if printed:
        outp.write("You must remove all debugging print statements from %s.\n" % repr(function))
        score -= 0.1
        if not step:
            return (FAIL_BAD_STYLE,max(0,score))
    
    return (TEST_SUCCESS,max(0,score))


def grade_func6(package,module,step=0,outp=sys.stdout):
    """
    Returns the test result and score for the implementation of get_for_id
    
    The step parameter is the phase in the grading pass.  Step 0 is a verification step
    and will stop at the first error found.  Otherwise it will continue through and try 
    to find all errors.
    
    Parameter package: The application package
    Precondition: package is a string
    
    Parameter module: The module to grade
    Precondition: module is a string
    
    Parameter step: The current verfication/grading step
    Precondition: grade is 0 or 1
    
    Parameter outp: The output stream
    Precondition: outp is a stream writer
    """
    score = 1
    env = import_module(package,module)
    function = 'get_for_id'
    
    if type(env) == str:
        outp.write(env)
        return (FAIL_CRASHES, 0)
    elif not hasattr(env.module,function):
        outp.write("File %s is missing the header for %s.\n" % (repr(module),repr(function)))
        return (FAIL_INCORRECT, 0)
    
    testcases = [('S00324',FILE1,FILE1[3]),
                 ('S00324',FILE1[1:],FILE1[3]),
                 ('S00843',FILE5,FILE5[8]),
                 ('811AX',FILE2,FILE2[2]),
                 ('XXXXXX',FILE1,None)]
    
    func = getattr(env.module,function)
    printed = False
    for data in testcases:
        short = repr(data[1])[:10]+'...'
        try:
            env.reset()
            received = func(*data[:2])
            expected = data[2]
            if received != expected:
                outp.write("The call %s(%s,%s) returns %s, not %s.\n" % (function, repr(data[0]), short, repr(received), repr(expected)))
                score -= 0.5/len(testcases)
                if not step:
                    return (FAIL_INCORRECT,max(0,score))
            if len(env.printed) != 0:
                printed = True
        except:
            import traceback
            outp.write("The call %s(%s,%s) crashed.\n" % (function, repr(data[0]), short))
            outp.write(traceback.format_exc()+'\n')
            score -= 0.5/len(testcases)
            if not step:
                return (FAIL_INCORRECT,max(0,score))
    if printed:
        outp.write("You must remove all debugging print statements from %s.\n" % repr(function))
        score -= 0.1
        if not step:
            return (FAIL_BAD_STYLE,max(0,score))
    
    return (TEST_SUCCESS,max(0,score))

pass
#mark -
#mark Graders
def grade_module(package,module,outp=sys.stdout):
    """
    Grades the utility package
    
    Parameter package: The application package
    Precondition: package is a string
    
    Parameter module: The module to grade
    Precondition: module is a string
    
    Parameter outp: The output stream
    Precondition: outp is a stream writer
    """
    
    outp.write('Docstring comments:\n')
    status, p = grade_docstring(package,module,1,outp)
    if p == 1:
        outp.write('The module docstring looks good.\n\n')
    else:
        outp.write('\n')
    
    crashes = status
    score = []
    score.append(p)
    
    functions = [('read_csv',grade_func1),  
                 ('write_csv',grade_func2),
                 ('read_json',grade_func3), 
                 ('str_to_time',grade_func4),
                 ('daytime',grade_func5),   
                 ('get_for_id',grade_func6)]
    
    for item in functions:
        if not crashes:
            outp.write("Comments for %s:\n" % repr(item[0]))
            status, p = item[1](package,module,1,outp)
            if p == 1:
                outp.write('The function looks good.\n\n')
            else:
                outp.write('\n')
            score.append(p)
        else:
            score.append(0)
    
    total  = 0.05*score[0]
    factor =  0.95/(len(score)-1)
    for item in score[1:]:
        total += item*factor
    
    return round(total,3)


def grade(outp=sys.stdout):
    """
    Invokes this subgrader (returning a percentage)
    """
    return grade_module('auditor','utils.py',outp)


if __name__ == '__main__':
    print(grade())