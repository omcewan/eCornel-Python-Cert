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


def dictify(table):
    """
    Returns a dictionary form of a table, using the first column as keys.
    
    Parameter table: The table to convert
    Precondition: table is a 2d table where the first column of each row is unique
    """
    result = {}
    for item in table:
        result[item[0]] = item
    return result


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
    Returns the test result and score for the implementation of teaches_multiengine
    
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
    function = 'teaches_multiengine'
    
    # Add extra newline to ensure the message lines up with the green/red result symbol
    outp.write("\n")

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
    
    utils = env.module.utils
    fpath = os.path.join(*TESTFILES,'instructors.csv')
    table = utils.read_csv(fpath)
    possibiles = len(table)-1
    
    # Relevant instructors
    teachers = { 'I003', 'I010', 'I096'}
    
    # CHECK THE TEST CASES
    func = getattr(env.module,function)
    printed = False
    for row in table[1:]:
        expct =  row[0] in teachers
        try:
            env.reset()
            answr = func(row)
            data = (function,repr(row),repr(answr),repr(expct))
            if expct != answr:
                outp.write('%s(%s) returned %s, not %s.\n' % data)
                score -= 1/possibiles
                if not step:
                    return (FAIL_INCORRECT,max(0,score))
            if len(env.printed) != 0:
                printed = True
        except:
            import traceback
            outp.write("The call %s(%s) crashed.\n" % (function, repr(row)))
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
    Returns the test result and score for the implementation of teaches_instrument
    
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
    function = 'teaches_instrument'
    
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
    
    utils = env.module.utils
    fpath = os.path.join(*TESTFILES,'instructors.csv')
    table = utils.read_csv(fpath)
    possibiles = len(table)-1
    
    # Relevant instructors
    teachers = { 'I003', 'I010', 'I032', 'I077', 'I097', 'I060'}
    
    # CHECK THE TEST CASES
    func = getattr(env.module,function)
    printed = False
    for row in table[1:]:
        expct =  row[0] in teachers
        try:
            env.reset()
            answr = func(row)
            data = (function,repr(row),repr(answr),repr(expct))
            if expct != answr:
                outp.write('%s(%s) returned %s, not %s.\n' % data)
                score -= 1/possibiles
                if not step:
                    return (FAIL_INCORRECT,max(0,score))
            if len(env.printed) != 0:
                printed = True
        except:
            import traceback
            outp.write("The call %s(%s) crashed.\n" % (function, repr(row)))
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
    Returns the test result and score for the implementation of is_advanced
    
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
    function = 'is_advanced'
    
    # Add extra newline to ensure the message lines up with the green/red result symbol
    outp.write("\n")

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
    
    utils = env.module.utils
    fpath = os.path.join(*TESTFILES,'fleet.csv')
    table = utils.read_csv(fpath)
    possibiles = len(table)-1
    
    # Relevant planes
    planes = { '446BU', '385AT', '249SM', '625LT', '436MK'}
    
    # CHECK THE TEST CASES
    func = getattr(env.module,function)
    printed = False
    for row in table[1:]:
        expct =  row[0] in planes
        try:
            env.reset()
            answr = func(row)
            data = (function,repr(row),repr(answr),repr(expct))
            if expct != answr:
                outp.write('%s(%s) returned %s, not %s.\n' % data)
                score -= 1/possibiles
                if not step:
                    return (FAIL_INCORRECT,max(0,score))
            if len(env.printed) != 0:
                printed = True
        except:
            import traceback
            outp.write("The call %s(%s) crashed.\n" % (function, repr(row)))
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
    Returns the test result and score for the implementation of is_multiengine
    
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
    function = 'is_multiengine'
    
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
    
    utils = env.module.utils
    fpath = os.path.join(*TESTFILES,'fleet.csv')
    table = utils.read_csv(fpath)
    possibiles = len(table)-1
    
    # Relevant planes
    planes = {'625LT'}
    
    # CHECK THE TEST CASES
    func = getattr(env.module,function)
    printed = False
    for row in table[1:]:
        expct =  row[0] in planes
        try:
            env.reset()
            answr = func(row)
            data = (function,repr(row),repr(answr),repr(expct))
            if expct != answr:
                outp.write('%s(%s) returned %s, not %s.\n' % data)
                score -= 1/possibiles
                if not step:
                    return (FAIL_INCORRECT,max(0,score))
            if len(env.printed) != 0:
                printed = True
        except:
            import traceback
            outp.write("The call %s(%s) crashed.\n" % (function, repr(row)))
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


def grade_func5(package,module,step=0,outp=sys.stdout):
    """
    Returns the test result and score for the implementation of is_ifr_capable
    
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
    function = 'is_ifr_capable'
    
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
    
    utils = env.module.utils
    fpath = os.path.join(*TESTFILES,'fleet.csv')
    table = utils.read_csv(fpath)
    possibiles = len(table)-1
    
    # Relevant planes
    planes = { '684TM', '254SE', '157ZA', '548QR', '217PQ', '446BU', '385AT', 
               '249SM', '625LT', '436MK'}
    
    # CHECK THE TEST CASES
    func = getattr(env.module,function)
    printed = False
    for row in table[1:]:
        expct =  row[0] in planes
        try:
            env.reset()
            answr = func(row)
            data = (function,repr(row),repr(answr),repr(expct))
            if expct != answr:
                outp.write('%s(%s) returned %s, not %s.\n' % data)
                score -= 1/possibiles
                if not step:
                    return (FAIL_INCORRECT,max(0,score))
            if len(env.printed) != 0:
                printed = True
        except:
            import traceback
            outp.write("The call %s(%s) crashed.\n" % (function, repr(row)))
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
    Returns the test result and score for the implementation of bad_endorsement
    
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
    function = 'bad_endorsement'
    
    # Add extra newline to ensure the message lines up with the green/red result symbol
    outp.write("\n")

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
    fpath  = os.path.join(*TESTFILES,'fleet.csv')
    planes = dictify(utils.read_csv(fpath))
    fpath  = os.path.join(*TESTFILES,'instructors.csv')
    teachers = dictify(utils.read_csv(fpath))
    fpath  = os.path.join(*TESTFILES,'students.csv')
    students = dictify(utils.read_csv(fpath))
    
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
    
    # CHECK THE TEST CASES
    func = getattr(env.module,function)
    printed = False
    for test in tests:
        expct = test[-1]
        teach = None if test[2] is None else teachers[test[2]]
        stud  = students[test[0]]
        plan  = planes[test[1]]
        load = False
        try:
            env.reset()
            time  = utils.str_to_time(test[3])
            load = True
            answr = func(time,stud,teach,plan)
            if expct != answr:
                data = (function,repr((time,stud,teach,plan)),repr(answr),repr(expct))
                outp.write('%s(%s) returned %s, not %s.\n' % data)
                score -= 1/len(tests)
                if not step:
                    return (FAIL_INCORRECT,max(0,score))
            if len(env.printed) != 0:
                printed = True
        except:
            import traceback
            if not load:
                outp.write("The call %s(%s) crashed.\n" % ('utils.str_to_time', repr(test[3])))
            else:
                args = repr((time,stud,teach,plan))
                outp.write("The call %s(%s) crashed.\n" % (function, args))
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


def grade_func7(package,module,step=0,outp=sys.stdout):
    """
    Returns the test result and score for the implementation of bad_ifr
    
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
    function = 'bad_ifr'
    
    # Add extra newline to ensure the message lines up with the green/red result symbol
    outp.write("\n")

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
    fpath  = os.path.join(*TESTFILES,'fleet.csv')
    planes = dictify(utils.read_csv(fpath))
    fpath  = os.path.join(*TESTFILES,'instructors.csv')
    teachers = dictify(utils.read_csv(fpath))
    fpath  = os.path.join(*TESTFILES,'students.csv')
    students = dictify(utils.read_csv(fpath))
    
    tests = [('S00811','811AX','I077','2017-01-07T10:00:00-05:00',True),
             ('S00811','157ZA','I072','2017-01-07T10:00:00-05:00',True),
             ('S00811','157ZA','I077','2017-01-07T10:00:00-05:00',False),
             ('S00850','426JQ','I032','2017-01-17T14:00:00-05:00',True),
             ('S00789','548QR','I032','2017-08-01T14:00:00-05:00',False),
             ('S00789','811AX','I032','2017-08-01T14:00:00-05:00',True),
             ('S00789','548QR',None,'2017-08-02T14:00:00-05:00',True),
             ('S00789','811AX',None,'2017-08-03T14:00:00-05:00',True),
             ('S00789','548QR',None,'2017-08-03T14:00:00-05:00',False)]
    
    # CHECK THE TEST CASES
    func = getattr(env.module,function)
    printed = False
    for test in tests:
        expct = test[-1]
        teach = None if test[2] is None else teachers[test[2]]
        stud  = students[test[0]]
        plan  = planes[test[1]]
        load = False
        try:
            env.reset()
            time  = utils.str_to_time(test[3])
            load = True
            answr = func(time,stud,teach,plan)
            if expct != answr:
                data = (function,repr((time,stud,teach,plan)),repr(answr),repr(expct))
                outp.write('%s(%s) returned %s, not %s.\n' % data)
                score -= 1/len(tests)
                if not step:
                    return (FAIL_INCORRECT,max(0,score))
            if len(env.printed) != 0:
                printed = True
        except:
            import traceback
            if not load:
                outp.write("The call %s(%s) crashed.\n" % ('utils.str_to_time', repr(test[3])))
            else:
                args = repr((time,stud,teach,plan))
                outp.write("The call %s(%s) crashed.\n" % (function, args))
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

def grade_func8(package,module,step=0,outp=sys.stdout):
    """
    Returns the test result and score for the implementation of list_endorsement_violations
    
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
    function = 'list_endorsement_violations'
    
    # Add extra newline to ensure the message lines up with the green/red result symbol
    outp.write("\n")
    
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
    fpath   = os.path.join(*TESTFILES,'badpilots.csv')
    correct = utils.read_csv(fpath)[1:]
    
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
            message = '%s(%s) identified flight %s for pilot %s, even though it is okay.' % data
            if results[key][-1].upper() == 'IFR' and results[key][5] == 'VFR':
                message += '\nThis is a VFR flight and cannot have an IFR violation.\n'
            outp.write(message)
            score -= 0.05
            if not step:
                return (FAIL_INCORRECT,max(0,score))
    
    for key in correct:
        if correct[key][-1] != results[key][-1]:
            data = (function,repr(tdir),correct[key][3],correct[key][0],
                    repr(results[key][-1]),repr(correct[key][-1]))
            message = "%s(%s)  identified flight %s for pilot %s as %s, not %s." % data
            if results[key][-1] in ['IFR', 'Credentials'] and results[key][5] == 'VFR':
                message += '\nThis is a VFR flight and cannot have an IFR violation.\n'
            outp.write(message)
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
    
    functions = [('teaches_multiengine',grade_func1),
                 ('teaches_instrument', grade_func2),
                 ('is_advanced',        grade_func3),
                 ('is_multiengine',     grade_func4),
                 ('is_ifr_capable',     grade_func5),
                 ('bad_endorsement',    grade_func6),
                 ('bad_ifr',            grade_func7),
                 ('list_endorsement_violations', grade_func8)]
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
    return grade_module('auditor','endorsements.py',outp)


if __name__ == '__main__':
    print(grade())