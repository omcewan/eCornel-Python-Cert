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


#mark -
#mark Helpers
DEPENDENCIES = ['utils','pilots']


def import_module(package,name,step=0):
    """
    Returns a reference to the module.
    
    Returns an error message if it fails.
    
    Parameter name: The module name
    Precondition: name is a string
    """
    # BOOTSTRAP
    import types
    depends = {}
    for item in DEPENDENCIES:
        try:
            environment = Environment(item,WORKSPACE+[package])
            for mod in depends:
                environment.capture(mod,depends[mod])
            if not environment.execute():
                message = 'Unable to import %s:\n' % item
                message = message+'\n'.join(environment.printed)+'\n'
                return message
            depends[item] = environment.module
        except Exception as e:
            msg = traceback.format_exc(0)
            pos2 = msg.find('^')
            pos1 = msg.rfind(')',0,pos2)
            if 'SyntaxError: unexpected EOF' in msg or 'IndentationError' in msg:
                msg = 'Remember to include and indent the docstring properly.\n'+msg
            elif pos1 != -1 and pos2 != -1 and not msg[pos1+1:pos2].strip():
                msg = 'Remember to end the header with a colon.\n'+msg
            else:
                msg = ("File %s has a major syntax error.\n" % repr(item+'.py'))+msg
            return msg
    try:
        refs = os.path.splitext(name)[0]
        environment = Environment(refs,WORKSPACE+[package])
        for mod in depends:
            environment.capture(mod,depends[mod])
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
            msg = ("File %s has a major syntax error.\n" % repr(item+'.py'))+msg
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
    Returns the test result and score for the implementation of bad_visibility
    
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
    function = 'bad_visibility'
    
    if type(env) == str:
        outp.write(env)
        return (FAIL_CRASHES, 0)
    elif not hasattr(env.module,function):
        outp.write("File %s is missing the header for %s.\n" % (repr(module),repr(function)))
        return (FAIL_INCORRECT, 0)
    else:
        for item in DEPENDENCIES:
            if not hasattr(env.module,item):
                outp.write("File %s is does not import %s.\n" % (repr(module),repr(item)))
                return (FAIL_INCORRECT, 0)
    
    utils  = env.module.utils
    fpath  = os.path.join(*TESTFILES,'weather.json')
    report = utils.read_json(fpath)
    
    minimums = [0.75,1,2,3,5,8,10]
    keys = [("2017-12-31T15:00:00-05:00",6), ("2017-12-31T14:00:00-05:00",2),
            ('2017-12-31T13:00:00-05:00',0), ('2017-12-30T09:00:00-05:00',1),
            ('2018-01-01T00:00:00-05:00',2), ('2017-12-31T01:00:00-05:00',3),
            ('2017-12-31T22:00:00-05:00',4), ('2017-12-31T03:00:00-05:00',5),
            ('2016-12-31T01:00:00-05:00',0),('2017-12-31T21:00:00-05:00',-1)]
    possibiles = len(minimums)*len(keys)
    
    # CHECK THE TEST CASES
    func = getattr(env.module,function)
    printed = False
    for key in keys:
        visibility = report[key[0]]['visibility'] if report else None
        for pos in range(len(minimums)):
            expt = key[1] != -1 and key[1] <= pos
            try:
                env.reset()
                test = func(visibility,minimums[pos])
                if test != expt:
                    data = (function,repr(visibility),repr(minimums[pos]),repr(test),repr(expt))
                    outp.write('%s(%s,%s) returned %s, but should have returned %s.\n' % data)
                    score -= 1/possibiles
                    if not step:
                        return (FAIL_INCORRECT,max(0,score))
                if len(env.printed) != 0:
                    printed = True
            except:
                import traceback
                outp.write("The call %s(%s,%s) crashed.\n" % (function, repr(visibility),repr(minimums[pos])))
                outp.write(traceback.format_exc()+'\n')
                score -= 1/possibiles
                if not step:
                    return (FAIL_INCORRECT,max(0,score))
    
    if printed:
        outp.write("You must remove all debugging print statements from %s.\n" % repr(function))
        score -= 0.1
        if not step:
            return (FAIL_BAD_STYLE,max(0,score))
    
    return (TEST_SUCCESS,max(0,score))


def grade_func2(package,module,step=0,outp=sys.stdout):
    """
    Returns the test result and score for the implementation of bad_winds
    
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
    function = 'bad_winds'
    
    if type(env) == str:
        outp.write(env)
        return (FAIL_CRASHES, 0)
    elif not hasattr(env.module,function):
        outp.write("File %s is missing the header for %s.\n" % (repr(module),repr(function)))
        return (FAIL_INCORRECT, 0)
    else:
        for item in DEPENDENCIES:
            if not hasattr(env.module,item):
                outp.write("File %s is does not import %s.\n" % (repr(module),repr(item)))
                return (FAIL_INCORRECT, 0)
    
    utils  = env.module.utils
    fpath  = os.path.join(*TESTFILES,'weather.json')
    report = utils.read_json(fpath)
    
    minimums = [(30,20),(25,15),(20,10),(20,8),(10,5)]
    keys =[("2017-06-20T13:00:00-04:00",0), ('2017-12-25T13:00:00-05:00',0), 
           ('2017-12-25T15:00:00-05:00',1), ('2017-12-30T21:00:00-05:00',2),
           ('2017-12-31T20:00:00-05:00',3), ('2018-01-01T00:00:00-05:00',4),
           ('2017-12-31T06:00:00-05:00',5), ("2017-10-12T11:00:00-04:00",0),
           ('2017-05-09T07:00:00-04:00',5) ]
    possibiles = len(minimums)*len(keys)
    
    # CHECK THE TEST CASES
    func = getattr(env.module,function)
    printed = False
    for key in keys:
        winds = report[key[0]]['wind'] if report else None
        for pos in range(len(minimums)):
            expt = key[1] != -1 and key[1] <= pos
            try:
                env.reset()
                test = func(winds,*minimums[pos])
                if test != expt:
                    data = (function,repr(winds),repr(minimums[pos][0]),repr(minimums[pos][1]),repr(test),repr(expt))
                    outp.write('%s(%s,%s,%s) returned %s, but should have returned %s.\n' % data)
                    score -= 1/possibiles
                    if not step:
                        return (FAIL_INCORRECT,max(0,score))
                if len(env.printed) != 0:
                    printed = True
            except:
                import traceback
                outp.write("The call %s(%s,%s,%s) crashed.\n" % (function, repr(winds),repr(minimums[pos][0]),repr(minimums[pos][1])))
                outp.write(traceback.format_exc()+'\n')
                score -= 1/possibiles
                if not step:
                    return (FAIL_INCORRECT,max(0,score))
    
    if printed:
        outp.write("You must remove all debugging print statements from %s.\n" % repr(function))
        score -= 0.1
        if not step:
            return (FAIL_BAD_STYLE,max(0,score))
    
    return (TEST_SUCCESS,max(0,score))


def grade_func3(package,module,step=0,outp=sys.stdout):
    """
    Returns the test result and score for the implementation of bad_ceiling
    
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
    function = 'bad_ceiling'
    
    if type(env) == str:
        outp.write(env)
        return (FAIL_CRASHES, 0)
    elif not hasattr(env.module,function):
        outp.write("File %s is missing the header for %s.\n" % (repr(module),repr(function)))
        return (FAIL_INCORRECT, 0)
    else:
        for item in DEPENDENCIES:
            if not hasattr(env.module,item):
                outp.write("File %s is does not import %s.\n" % (repr(module),repr(item)))
                return (FAIL_INCORRECT, 0)
    
    utils  = env.module.utils
    fpath  = os.path.join(*TESTFILES,'weather.json')
    report = utils.read_json(fpath)
    
    minimums = [500,1000,1500,2000,2500,3000,3500,5000]
    keys =[("2017-12-30T19:00:00-05:00",-1),("2017-10-31T12:00:00-04:00",0),
           ('2017-12-23T22:00:00-05:00',0), ('2017-12-31T12:00:00-05:00',1),
           ('2018-01-01T00:00:00-05:00',2), ('2017-12-31T21:00:00-05:00',3),
           ('2017-12-31T20:00:00-05:00',4), ('2017-12-31T02:00:00-05:00',5),
           ('2017-12-31T01:00:00-05:00',6), ('2017-12-30T18:00:00-05:00',7),
           ('2017-12-30T20:00:00-05:00',-1),("2017-10-12T11:00:00-04:00",-1),
           ('2017-06-05T12:00:00-04:00',-1)]
    possibiles = len(minimums)*len(keys)
    
    # CHECK THE TEST CASES
    func = getattr(env.module,function)
    printed = False
    for key in keys:
        sky = report[key[0]]['sky'] if report else None
        for pos in range(len(minimums)):
            expt = key[1] != -1 and key[1] <= pos
            try:
                env.reset()
                test = func(sky,minimums[pos])
                if test != expt:
                    data = (function,repr(sky),repr(minimums[pos]),repr(test),repr(expt))
                    outp.write('%s(%s,%s) returned %s, but should have returned %s.\n' % data)
                    score -= 1/possibiles
                    if not step:
                        return (FAIL_INCORRECT,max(0,score))
                if len(env.printed) != 0:
                    printed = True
            except:
                import traceback
                outp.write("The call %s(%s,%s) crashed.\n" % (function, repr(sky),repr(minimums[pos])))
                outp.write(traceback.format_exc()+'\n')
                score -= 1/possibiles
                if not step:
                    return (FAIL_INCORRECT,max(0,score))
    
    if printed:
        outp.write("You must remove all debugging print statements from %s.\n" % repr(function))
        score -= 0.1
        if not step:
            return (FAIL_BAD_STYLE,max(0,score))
    
    return (TEST_SUCCESS,max(0,score))


def grade_func4(package,module,step=0,outp=sys.stdout):
    """
    Returns the test result and score for the implementation of get_weather_report
    
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
    function = 'get_weather_report'
    
    if type(env) == str:
        outp.write(env)
        return (FAIL_CRASHES, 0)
    elif not hasattr(env.module,function):
        outp.write("File %s is missing the header for %s.\n" % (repr(module),repr(function)))
        return (FAIL_INCORRECT, 0)
    else:
        for item in DEPENDENCIES:
            if not hasattr(env.module,item):
                outp.write("File %s is does not import %s.\n" % (repr(module),repr(item)))
                return (FAIL_INCORRECT, 0)
    
    utils  = env.module.utils
    fpath  = os.path.join(*TESTFILES,'weather.json')
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
    
    # CHECK THE TEST CASES
    func = getattr(env.module,function)
    printed = False
    for test in tests:
        expct = report[test[1]] if report else None
        load = False
        try:
            stamp = utils.str_to_time(test[0])
            load = True
            found = func(stamp,report)
            if expct != found:
                try:
                    code = 'code='+repr(found['code'])
                except:
                    code = 'no code'
                data  = (function,test[0],'weather',code,repr(expct['code']))
                outp.write('%s(%s,%s) returned a report with %s, not code=%s.\n' % data)
                score -= 1/len(tests)
                if not step:
                    return (FAIL_INCORRECT,max(0,score))
            if len(env.printed) != 0:
                printed = True
        except:
            import traceback
            outp.write("The call %s(%s,%s) crashed.\n" % (function, test[0], 'weather'))
            outp.write(traceback.format_exc()+'\n')
            score -= 1/len(tests)
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
    Returns the test result and score for the implementation of get_weather_violation
    
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
    function = 'get_weather_violation'
    
    if type(env) == str:
        outp.write(env)
        return (FAIL_CRASHES, 0)
    elif not hasattr(env.module,function):
        outp.write("File %s is missing the header for %s.\n" % (repr(module),repr(function)))
        return (FAIL_INCORRECT, 0)
    else:
        for item in DEPENDENCIES:
            if not hasattr(env.module,item):
                outp.write("File %s is does not import %s.\n" % (repr(module),repr(item)))
                return (FAIL_INCORRECT, 0)
    
    utils  = env.module.utils
    fpath  = os.path.join(*TESTFILES,'weather.json')
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
    possibiles = len(minimums)*len(tests)
    
    # CHECK THE TEST CASES
    func = getattr(env.module,function)
    printed = False
    for test in tests:
        for pos in range(len(minimums)):
            expct = test[pos+1]
            read  = report[test[0]] if report and test[0] in report else None
            try:
                check = func(read,minimums[pos])
                if expct != check:
                    data  = (function,repr(read),repr(minimums[pos]),repr(check),repr(expct))
                    outp.write('%s(%s,%s) returned %s, not %s.\n' % data)
                    score -= 1/possibiles
                    if not step:
                        return (FAIL_INCORRECT,max(0,score))
                if len(env.printed) != 0:
                    printed = True
            except:
                import traceback
                outp.write("The call %s(%s,%s) crashed.\n" % (function,repr(read),repr(minimums[pos])))
                outp.write(traceback.format_exc()+'\n')
                score -= 1/possibiles
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
    Returns the test result and score for the implementation of list_weather_violations
    
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
    function = 'list_weather_violations'
    
    
    if type(env) == str:
        outp.write(env)
        return (FAIL_CRASHES, 0)
    elif not hasattr(env.module,function):
        outp.write("File %s is missing the header for %s.\n" % (repr(module),repr(function)))
        return (FAIL_INCORRECT, 0)
    else:
        for item in DEPENDENCIES:
            if not hasattr(env.module,item):
                outp.write("File %s is does not import %s.\n" % (repr(module),repr(item)))
                return (FAIL_INCORRECT, 0)
    
    utils   = env.module.utils
    pilots  = env.module.pilots
    fpath   = os.path.join(*TESTFILES,'badweather.csv')
    correct = utils.read_csv(fpath)
    correct = correct[1:] if correct else None
    
    fpath   = os.path.join(*TESTFILES,'students.csv')
    students = utils.read_csv(fpath)
    
    func = getattr(env.module,function)
    tdir = os.path.join(*TESTFILES)
    printed = False
    results = []
    try:
        results = func(tdir)
        if len(env.printed) != 0:
            printed = True
    except:
        import traceback
        outp.write("The call %s(%s) crashed.\n" % (function,repr(tdir)))
        outp.write(traceback.format_exc()+'\n')
        return (FAIL_INCORRECT, 0)
    
    if results is None:
        outp.write('%s(%s) returned None.\n' % (function,repr(tdir)))
        return (FAIL_CRASHES, 0)
    
    # Hash for better comparison
    data = {}
    for item in results:
        data[item[0]+item[3]] = item
    results = data
    
    data = {}
    for item in correct:
        if len(item) != len(correct[0]):
            quit_with_error('%s is not a (1-dimensional) list with %d elements.' % (item,len(correct[0])))
        data[item[0]+item[3]] = item
    correct = data
    
    for key in correct:
        if not key in results:
            data = (function,repr(tdir),correct[key][3],correct[key][0])
            outp.write('%s(%s) is missing the flight %s for pilot %s.\n' % data)
            score -= 0.05
            if not step:
                return (FAIL_INCORRECT,max(0,score))
    
    for key in results:
        if not key in correct:
            data = (function,repr(tdir),results[key][3],results[key][0])
            outp.write('%s(%s) identified flight %s for pilot %s, even though it is okay.\n' % data)
            
            # Give some better feedback
            indx = pilots.get_certification(utils.str_to_time(results[key][3]),
                                            utils.get_for_id(results[key][0],students))
            cert = ['a novice pilot','a student pilot','a certified pilot',
                    'a pilot with 50 hours experience','a unregistered pilot'][indx]
            sups = "dual instruction" if results[key][2] else cert
            cond = 'VMC' if results[key][5] == 'VFR' else 'IMC'
            outp.write('This is a %s flight with %s in %s conditions.\n' % (results[key][6],sups,cond))
            
            score -= 0.05
            if not step:
                return (FAIL_INCORRECT,max(0,score))
    
    for key in correct:
        if correct[key][-1] != results[key][-1]:
            data = (function,repr(tdir),correct[key][3],correct[key][0],
                    repr(results[key][-1]),repr(correct[key][-1]))
            outp.write("%s(%s)  identified flight %s for pilot %s as %s, not %s.\n" % data)
            
            # Give some better feedback
            indx = pilots.get_certification(utils.str_to_time(results[key][3]),
                                            utils.get_for_id(results[key][0],students))
            cert = ['a novice pilot','a student pilot','a certified pilot',
                    'a pilot with 50 hours experience','a unregistered pilot'][indx]
            sups = "dual instruction" if results[key][2] else cert
            cond = 'VMC' if results[key][5] == 'VFR' else 'IMC'
            outp.write('This is a %s flight with %s in %s conditions.\n' % (results[key][6],sups,cond))
            
            score -= 0.05
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
    
    functions = [('bad_visibility',grade_func1),
                 ('bad_winds',grade_func2),
                 ('bad_ceiling',grade_func3),
                 ('get_weather_report',grade_func4),
                 ('get_weather_violation',grade_func5),
                 ('list_weather_violations',grade_func6)]
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
    return grade_module('auditor','violations.py',outp)


if __name__ == '__main__':
    print(grade())