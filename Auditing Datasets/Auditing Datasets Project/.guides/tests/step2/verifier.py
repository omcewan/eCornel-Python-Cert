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
import random
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
DEPENDENCIES = ['utils']

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


def cert_to_name(cert):
    """
    Returns a string describing a certification.
    
    Parameter cert: The certification
    Precondition: cert is an int and one of PILOT_INVALID, PILOT_NOVICE, PILOT_STUDENT,
    PILOT_CERTIFIED, PILOT_50_HOURS
    """
    if cert == -1:
        return 'PILOT_INVALID'
    elif cert == 0:
        return 'PILOT_NOVICE'
    elif cert == 1:
        return 'PILOT_STUDENT'
    elif cert == 2:
        return 'PILOT_CERTIFIED'
    elif cert == 3:
        return 'PILOT_50_HOURS'
    return cert


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
    Returns the test result and score for the implementation of get_certification
    
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
    function = 'get_certification'
    
    if type(env) == str:
        outp.write(env)
        return (FAIL_CRASHES, 0)
    elif not hasattr(env.module,function):
        outp.write("File %s is missing the header for %s.\n" % (repr(module),repr(function)))
        return (FAIL_INCORRECT, 0)
    else:
        for item in DEPENDENCIES:
            if not hasattr(env.module,item):
                outp.write("File %s does not import %s.\n" % (repr(module),repr(item)))
                return (FAIL_INCORRECT, 0)
    
    utils = env.module.utils
    fpath = os.path.join(*TESTFILES,'students.csv')
    table = utils.read_csv(fpath)
    
    takeoffs = ['2015-01-14T08:00:00','2015-07-15T10:15:20','2015-07-16T10:15:20',
                '2015-10-08T12:30:45','2016-02-15T20:35:16','2017-12-30 16:30:45']
    students = {'S00313' : ( 0,1,1,1,1,1),
                'S00331' : (-1,0,0,0,1,1),
                'S00353' : (-1,2,2,3,3,3),
                'S00362' : (-1,1,1,2,3,3),
                'S00378' : (-1,0,1,2,3,3),
                'S01139' : (-1,-1,-1,-1,-1,0)}
    possibiles = len(takeoffs)*len(students)
    
    # CHECK THE TEST CASES
    func = getattr(env.module,function)
    printed = False
    for person in students:
        for pos in range(len(takeoffs)):
            load = 0
            try:
                env.reset()
                row  = utils.get_for_id(person,table)
                load = 1
                time = utils.str_to_time(takeoffs[pos], "America/New_York")
                load = 2
                cert = func(time,row)
                if students[person][pos] != cert:
                    data = (function,person,repr(cert_to_name(cert)),takeoffs[pos],repr(cert_to_name(students[person][pos])))
                    outp.write('%s marked %s as %s on %s, but was really %s.\n' % data)
                    score -= 1/possibiles
                    if not step:
                        return (FAIL_INCORRECT,max(0,score))
                if len(env.printed) != 0:
                    printed = True
            except:
                import traceback
                if load == 0:
                    outp.write("The call %s(%s,students) crashed.\n" % ('utils.get_for_id', repr(person)))
                elif load == 0:
                    outp.write("The call %s(%s) crashed.\n" % ('utils.str_to_time', repr(takeoffs[pos])))
                else:
                    outp.write("The call %s(%s,%s) crashed.\n" % (function, takeoffs[pos], repr(row)))
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
    Returns the test result and score for the implementation of has_instrument_rating
    
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
    function = 'has_instrument_rating'
    
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
                outp.write("File %s does not import %s.\n" % (repr(module),repr(item)))
                return (FAIL_INCORRECT, 0)
    
    utils = env.module.utils
    fpath = os.path.join(*TESTFILES,'students.csv')
    table = utils.read_csv(fpath)
    
    takeoffs = ['2015-12-11T08:00:00','2015-12-27T10:15:20','2015-12-28T10:15:20','2016-04-18T12:30:45']
    students = {'S00313' : ( False, False, False, False),
                'S00350' : ( False, True, True, True),
                'S00369' : ( False, False, True, True),
                'S00378' : ( False, False, False, True)}
    possibiles = len(takeoffs)*len(students)
    
    func = getattr(env.module,function)
    printed = False
    for person in students:
        for pos in range(len(takeoffs)):
            load = 0
            try:
                env.reset()
                row  = utils.get_for_id(person,table)
                load = 1
                time = utils.str_to_time(takeoffs[pos])
                load = 2
                rate = func(time,row)
                if students[person][pos] != rate:
                    data = (function,person,repr(rate),takeoffs[pos],repr(students[person][pos]))
                    outp.write('%s marked %s as %s on %s, but was really %s.\n' % data)
                    score -= 1/possibiles
                    if not step:
                        return (FAIL_INCORRECT,max(0,score))
                if len(env.printed) != 0:
                    printed = True
            except:
                import traceback
                if load == 0:
                    outp.write("The call %s(%s,students) crashed.\n" % ('utils.get_for_id', repr(person)))
                elif load == 0:
                    outp.write("The call %s(%s) crashed.\n" % ('utils.str_to_time', repr(takeoffs[pos])))
                else:
                    outp.write("The call %s(%s,%s) crashed.\n" % (function, takeoffs[pos], repr(row)))
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
    Returns the test result and score for the implementation of has_advanced_endorsement
    
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
    function = 'has_advanced_endorsement'
    
    if type(env) == str:
        outp.write(env)
        return (FAIL_CRASHES, 0)
    elif not hasattr(env.module,function):
        outp.write("File %s is missing the header for %s.\n" % (repr(module),repr(function)))
        return (FAIL_INCORRECT, 0)
    else:
        for item in DEPENDENCIES:
            if not hasattr(env.module,item):
                outp.write("File %s does not import %s.\n" % (repr(module),repr(item)))
                return (FAIL_INCORRECT, 0)
    
    utils = env.module.utils
    fpath = os.path.join(*TESTFILES,'students.csv')
    table = utils.read_csv(fpath)
    
    takeoffs = ['2015-12-20T08:00:00','2016-05-31T10:15:20','2016-12-05T12:30:45','2016-12-12T10:15:20',]
    students = {'S00313' : ( False, False, False, False),
                'S00369' : ( False, False, False, False),
                'S00378' : ( False, True, True, True),
                'S00436' : ( False, False, True, True),
                'S00536' : ( False, False, False, True)}
    possibiles = len(takeoffs)*len(students)
    
    func = getattr(env.module,function)
    printed = False
    for person in students:
        for pos in range(len(takeoffs)):
            load = 0
            try:
                env.reset()
                row  = utils.get_for_id(person,table)
                load = 1
                time = utils.str_to_time(takeoffs[pos])
                load = 2
                rate = func(time,row)
                if students[person][pos] != rate:
                    data = (function,person,repr(rate),takeoffs[pos],repr(students[person][pos]))
                    outp.write('%s marked %s as %s on %s, but was really %s.\n' % data)
                    score -= 1/possibiles
                    if not step:
                        return (FAIL_INCORRECT,max(0,score))
                if len(env.printed) != 0:
                    printed = True
            except:
                import traceback
                if load == 0:
                    outp.write("The call %s(%s,students) crashed.\n" % ('utils.get_for_id', repr(person)))
                elif load == 0:
                    outp.write("The call %s(%s) crashed.\n" % ('utils.str_to_time', repr(takeoffs[pos])))
                else:
                    outp.write("The call %s(%s,%s) crashed.\n" % (function, takeoffs[pos], repr(row)))
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
    Returns the test result and score for the implementation of has_multiengine_endorsement
    
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
    function = 'has_multiengine_endorsement'
    
    if type(env) == str:
        outp.write(env)
        return (FAIL_CRASHES, 0)
    elif not hasattr(env.module,function):
        outp.write("File %s is missing the header for %s.\n" % (repr(module),repr(function)))
        return (FAIL_INCORRECT, 0)
    else:
        for item in DEPENDENCIES:
            if not hasattr(env.module,item):
                outp.write("File %s does not import %s.\n" % (repr(module),repr(item)))
                return (FAIL_INCORRECT, 0)
    
    utils = env.module.utils
    fpath = os.path.join(*TESTFILES,'students.csv')
    table = utils.read_csv(fpath)
    
    takeoffs = ['2015-12-11T08:00:00','2017-09-27T10:15:20','2017-09-28T10:15:20','2017-11-05T12:30:45']
    students = {'S00313' : ( False, False, False, False),
                'S00378' : ( False, False, True, True),
                'S00436' : ( False, False, False, True),
                'S00536' : ( False, False, False, False) }
    possibiles = len(takeoffs)*len(students)
    
    func = getattr(env.module,function)
    printed = False
    for person in students:
        for pos in range(len(takeoffs)):
            load = 0
            try:
                env.reset()
                row  = utils.get_for_id(person,table)
                load = 1
                time = utils.str_to_time(takeoffs[pos])
                load = 2
                rate = func(time,row)
                if students[person][pos] != rate:
                    data = (function,person,repr(rate),takeoffs[pos],repr(students[person][pos]))
                    outp.write('%s marked %s as %s on %s, but was really %s.\n' % data)
                    score -= 1/possibiles
                    if not step:
                        return (FAIL_INCORRECT,max(0,score))
                if len(env.printed) != 0:
                    printed = True
            except:
                import traceback
                if load == 0:
                    outp.write("The call %s(%s,students) crashed.\n" % ('utils.get_for_id', repr(person)))
                elif load == 0:
                    outp.write("The call %s(%s) crashed.\n" % ('utils.str_to_time', repr(takeoffs[pos])))
                else:
                    outp.write("The call %s(%s,%s) crashed.\n" % (function, takeoffs[pos], repr(row)))
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
    Returns the test result and score for the implementation of get_best_value
    
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
    function = 'get_best_value'
    
    if type(env) == str:
        outp.write(env)
        return (FAIL_CRASHES, 0)
    elif not hasattr(env.module,function):
        outp.write("File %s is missing the header for %s.\n" % (repr(module),repr(function)))
        return (FAIL_INCORRECT, 0)
    else:
        for item in DEPENDENCIES:
            if not hasattr(env.module,item):
                outp.write("File %s does not import %s.\n" % (repr(module),repr(item)))
                return (FAIL_INCORRECT, 0)
    
    # Embedded helper to display table
    def output_table(tbl, template=None):
        cols = len(tbl[0])
        outp.write("\n%s  Contents of table (all strings)  %s\n" % ("-"*18,"-"*18))
        for row in tbl:
            if template:
                outp.write(template.format(*row))
            else:
                for val in row:
                    outp.write("{:<6}".format(val))
                outp.write("\n")
        outp.write("-"*72 + "\n\n")

    # Load the first table from minimums.csv
    utils = env.module.utils
    fpath = os.path.join(*TESTFILES,'minimums.csv')
    table = utils.read_csv(fpath)[1:]

    # Expected answers for each of the indicated columns
    tests = { 4: (500.0, 5000.0),
              5: (0.75, 10.0),
              6: (20.0, 30.0),
              7: (8.0, 20.0) }
    # Check for both True (highest) and False (lowest)
    situations = ( (False, 0, 'lowest'),
                   (True, 1, 'highest') )
    possibiles = len(tests)*len(situations)

    func = getattr(env.module,function)
    printed = False

    # Test using minimums.cvs
    for col, bests in tests.items():
        for situ in situations:
            try:
                env.reset()
                best = func(table[1:],col,situ[0])
                if bests[situ[1]] != best:
                    data = (function,repr(best),situ[2], col, bests[situ[1]])
                    outp.write('%s returned %s as %s value for column position %s in minimums.csv, but should have returned %s' % data)
                    if type(best) != float:
                        outp.write('\nAlso, the return value is not a float, but a float is expected.\n')
                    output_table(table[1:], "{:<12} {:<6} {:<16} {:<8} {:<8} {:<6} {:<6} {:<6}\n")
                    score -= 1/possibiles
                    if not step:
                        return (FAIL_INCORRECT,max(0,score))
                if len(env.printed) != 0:
                    printed = True
            except:
                import traceback
                outp.write("The call %s(table,%s,%s) crashed.\n\n" % (function, repr(col), repr(situ[0])))
                outp.write(traceback.format_exc()+'\n')
                output_table(table[1:], "{:<12} {:<6} {:<16} {:<8} {:<8} {:<6} {:<6} {:<6}\n")
                score -= 1/possibiles
                if not step:
                    return (FAIL_INCORRECT,max(0,score))

    # Test 10 times using "random" tables of values
    import random
    for i in range(10):
        random.seed(i)
        # Generate random table
        cols = random.randint(3,6)
        rows = random.randint(7,14)
        rtable = [list(map(str,random.sample(range(99), cols))) for r in range(rows)]
        for col in range(cols):
            for situ in situations:
                try:
                    env.reset()
                    result = func(rtable,col,situ[0])
                    if situ[0]:
                        best = float(max(rtable, key=lambda x: float(x[col]))[col])
                    else:
                        best = float(min(rtable, key=lambda x: float(x[col]))[col])
                    if best != result:
                        data = (function,repr(result),situ[2], col, best)
                        outp.write('%s returned %s as %s value for column position %s, but should have returned %s' % data)
                        output_table(rtable)
                        score -= 1/possibiles
                        if not step:
                            return (FAIL_INCORRECT,max(0,score))
                        if len(env.printed) != 0:
                            printed = True
                except:
                    import traceback
                    outp.write("The call %s(table,%s,%s) crashed.\n\n" % (function, repr(col), repr(situ[0])))
                    outp.write(traceback.format_exc()+'\n')
                    output_table(rtable)
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
    Returns the test result and score for the implementation of get_minimums
    
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
    function = 'get_minimums'
    
    if type(env) == str:
        outp.write(env)
        return (FAIL_CRASHES, 0)
    elif not hasattr(env.module,function):
        outp.write("File %s is missing the header for %s.\n" % (repr(module),repr(function)))
        return (FAIL_INCORRECT, 0)
    else:
        for item in DEPENDENCIES:
            if not hasattr(env.module,item):
                outp.write("File %s does not import %s.\n" % (repr(module),repr(item)))
                return (FAIL_INCORRECT, 0)
    
    func = getattr(env.module,function)
    printed = False
    
    # Test the basics to catch hard-coding
    utils = env.module.utils
    fpath = os.path.join(*TESTFILES,'minimums.csv')
    table1 = utils.read_csv(fpath)
    
    # Test the alternates to catch hard-coding
    fpath = os.path.join(*TESTFILES,'alternates.csv')
    table2 = utils.read_csv(fpath)

    if (table1 is None or table2 is None):
        outp.write("Function read_csv cannot process the minimums table.")
        return (FAIL_INCORRECT, 0)
    
    pilots = env.module
    testcases = [(pilots.PILOT_INVALID,  'Pattern',      False,False,True, table1, None),
                 (pilots.PILOT_INVALID,  'Pattern',      True, False,True, table1, 21),
                 (pilots.PILOT_NOVICE,   'Pattern',      False,False,True, table1, None),
                 (pilots.PILOT_NOVICE,   'Pattern',      True, False,True, table1, 21),
                 (pilots.PILOT_STUDENT,  'Pattern',      False,False,True, table1, None),
                 (pilots.PILOT_STUDENT,  'Practice Area',False,False,True, table1, None),
                 (pilots.PILOT_STUDENT,  'Cross Country',False,False,True, table1, None),
                 (pilots.PILOT_STUDENT,  'Pattern',      False,True, True, table1, 1),
                 (pilots.PILOT_STUDENT,  'Practice Area',False,True, True, table1, 2),
                 (pilots.PILOT_STUDENT,  'Cross Country',False,True, True, table1, 3),
                 (pilots.PILOT_STUDENT,  'Pattern',      False,False,False,table1, None),
                 (pilots.PILOT_STUDENT,  'Practice Area',False,False,False,table1, None),
                 (pilots.PILOT_STUDENT,  'Cross Country',False,False,False,table1, None),
                 (pilots.PILOT_STUDENT,  'Pattern',      False,True, False,table1, None),
                 (pilots.PILOT_STUDENT,  'Practice Area',False,True, False,table1, None),
                 (pilots.PILOT_STUDENT,  'Cross Country',False,True, False,table1, None),
                 (pilots.PILOT_STUDENT,  'Pattern',      True,False,True,  table1, 21),
                 (pilots.PILOT_STUDENT,  'Practice Area',True,False,True,  table1, 21),
                 (pilots.PILOT_STUDENT,  'Cross Country',True,False,True,  table1, 21),
                 (pilots.PILOT_STUDENT,  'Pattern',      True,True, True,  table1, 14),
                 (pilots.PILOT_STUDENT,  'Practice Area',True,True, True,  table1, 15),
                 (pilots.PILOT_STUDENT,  'Cross Country',True,True, True,  table1, 16),
                 (pilots.PILOT_STUDENT,  'Pattern',      True,False,False, table1, 22),
                 (pilots.PILOT_STUDENT,  'Practice Area',True,False,False, table1, 22),
                 (pilots.PILOT_STUDENT,  'Cross Country',True,False,False, table1, 22),
                 (pilots.PILOT_STUDENT,  'Pattern',      True,True, False, table1, 17),
                 (pilots.PILOT_STUDENT,  'Practice Area',True,True, False, table1, 17),
                 (pilots.PILOT_STUDENT,  'Cross Country',True,True, False, table1, 18),
                 (pilots.PILOT_CERTIFIED,'Pattern',      False,False,True, table1, 19),
                 (pilots.PILOT_CERTIFIED,'Practice Area',False,False,True, table1, 19),
                 (pilots.PILOT_CERTIFIED,'Cross Country',False,False,True, table1, 19),
                 (pilots.PILOT_CERTIFIED,'Pattern',      False,True, True, table1, 4),
                 (pilots.PILOT_CERTIFIED,'Practice Area',False,True, True, table1, 5),
                 (pilots.PILOT_CERTIFIED,'Cross Country',False,True, True, table1, 6),
                 (pilots.PILOT_CERTIFIED,'Pattern',      False,False,False,table1, 20),
                 (pilots.PILOT_CERTIFIED,'Practice Area',False,False,False,table1, 20),
                 (pilots.PILOT_CERTIFIED,'Cross Country',False,False,False,table1, 20),
                 (pilots.PILOT_CERTIFIED,'Pattern',      False,True, False,table1, 7),
                 (pilots.PILOT_CERTIFIED,'Practice Area',False,True, False,table1, 7),
                 (pilots.PILOT_CERTIFIED,'Cross Country',False,True, False,table1, 8),
                 (pilots.PILOT_CERTIFIED,'Pattern',      True,False,True,  table1, 21),
                 (pilots.PILOT_CERTIFIED,'Practice Area',True,False,True,  table1, 21),
                 (pilots.PILOT_CERTIFIED,'Cross Country',True,False,True,  table1, 21),
                 (pilots.PILOT_CERTIFIED,'Pattern',      True,True, True,  table1, 14),
                 (pilots.PILOT_CERTIFIED,'Practice Area',True,True, True,  table1, 15),
                 (pilots.PILOT_CERTIFIED,'Cross Country',True,True, True,  table1, 16),
                 (pilots.PILOT_CERTIFIED,'Pattern',      True,False,False, table1, 22),
                 (pilots.PILOT_CERTIFIED,'Practice Area',True,False,False, table1, 22),
                 (pilots.PILOT_CERTIFIED,'Cross Country',True,False,False, table1, 22),
                 (pilots.PILOT_CERTIFIED,'Pattern',      True,True, False, table1, 17),
                 (pilots.PILOT_CERTIFIED,'Practice Area',True,True, False, table1, 17),
                 (pilots.PILOT_CERTIFIED,'Cross Country',True,True, False, table1, 18),
                 (pilots.PILOT_50_HOURS, 'Pattern',      False,False,True, table1, 19),
                 (pilots.PILOT_50_HOURS, 'Practice Area',False,False,True, table1, 19),
                 (pilots.PILOT_50_HOURS, 'Cross Country',False,False,True, table1, 19),
                 (pilots.PILOT_50_HOURS, 'Pattern',      False,True, True, table1, 9),
                 (pilots.PILOT_50_HOURS, 'Practice Area',False,True, True, table1, 10),
                 (pilots.PILOT_50_HOURS, 'Cross Country',False,True, True, table1, 11),
                 (pilots.PILOT_50_HOURS, 'Pattern',      False,False,False,table1, 20),
                 (pilots.PILOT_50_HOURS, 'Practice Area',False,False,False,table1, 20),
                 (pilots.PILOT_50_HOURS, 'Cross Country',False,False,False,table1, 20),
                 (pilots.PILOT_50_HOURS, 'Pattern',      False,True, False,table1, 12),
                 (pilots.PILOT_50_HOURS, 'Practice Area',False,True, False,table1, 12),
                 (pilots.PILOT_50_HOURS, 'Cross Country',False,True, False,table1, 13),
                 (pilots.PILOT_50_HOURS, 'Pattern',      True,False,True,  table1, 21),
                 (pilots.PILOT_50_HOURS, 'Practice Area',True,False,True,  table1, 21),
                 (pilots.PILOT_50_HOURS, 'Cross Country',True,False,True,  table1, 21),
                 (pilots.PILOT_50_HOURS, 'Pattern',      True,True, True,  table1, 14),
                 (pilots.PILOT_50_HOURS, 'Practice Area',True,True, True,  table1, 15),
                 (pilots.PILOT_50_HOURS, 'Cross Country',True,True, True,  table1, 16),
                 (pilots.PILOT_50_HOURS, 'Pattern',      True,False,False, table1, 22),
                 (pilots.PILOT_50_HOURS, 'Practice Area',True,False,False, table1, 22),
                 (pilots.PILOT_50_HOURS, 'Cross Country',True,False,False, table1, 22),
                 (pilots.PILOT_50_HOURS, 'Pattern',      True,True, False, table1, 17),
                 (pilots.PILOT_50_HOURS, 'Practice Area',True,True, False, table1, 17),
                 (pilots.PILOT_50_HOURS, 'Cross Country',True,True, False, table1, 18),
                 (pilots.PILOT_INVALID,  'Pattern',      False,False,True, table2, None),
                 (pilots.PILOT_INVALID,  'Pattern',      True, False,True, table2, 3),
                 (pilots.PILOT_NOVICE,   'Pattern',      False,False,True, table2, None),
                 (pilots.PILOT_NOVICE,   'Pattern',      True, False,True, table2, 3),
                 (pilots.PILOT_STUDENT,  'Pattern',      False,False,True, table2, None),
                 (pilots.PILOT_STUDENT,  'Practice Area',False,False,True, table2, None),
                 (pilots.PILOT_STUDENT,  'Cross Country',False,False,True, table2, None),
                 (pilots.PILOT_STUDENT,  'Pattern',      False,True, True, table2, 10),
                 (pilots.PILOT_STUDENT,  'Practice Area',False,True, True, table2, 8),
                 (pilots.PILOT_STUDENT,  'Cross Country',False,True, True, table2, 11),
                 (pilots.PILOT_STUDENT,  'Pattern',      False,False,False,table2, None),
                 (pilots.PILOT_STUDENT,  'Practice Area',False,False,False,table2, None),
                 (pilots.PILOT_STUDENT,  'Cross Country',False,False,False,table2, None),
                 (pilots.PILOT_STUDENT,  'Pattern',      False,True, False,table2, None),
                 (pilots.PILOT_STUDENT,  'Practice Area',False,True, False,table2, None),
                 (pilots.PILOT_STUDENT,  'Cross Country',False,True, False,table2, None),
                 (pilots.PILOT_STUDENT,  'Pattern',      True,False,True,  table2, 3),
                 (pilots.PILOT_STUDENT,  'Practice Area',True,False,True,  table2, 3),
                 (pilots.PILOT_STUDENT,  'Cross Country',True,False,True,  table2, 3),
                 (pilots.PILOT_STUDENT,  'Pattern',      True,True, True,  table2, 15),
                 (pilots.PILOT_STUDENT,  'Practice Area',True,True, True,  table2, 16),
                 (pilots.PILOT_STUDENT,  'Cross Country',True,True, True,  table2, 9),
                 (pilots.PILOT_STUDENT,  'Pattern',      True,False,False, table2, 4),
                 (pilots.PILOT_STUDENT,  'Practice Area',True,False,False, table2, 4),
                 (pilots.PILOT_STUDENT,  'Cross Country',True,False,False, table2, 4),
                 (pilots.PILOT_STUDENT,  'Pattern',      True,True, False, table2, 19),
                 (pilots.PILOT_STUDENT,  'Practice Area',True,True, False, table2, 19),
                 (pilots.PILOT_STUDENT,  'Cross Country',True,True, False, table2, 20),
                 (pilots.PILOT_CERTIFIED,'Pattern',      False,False,True, table2, 21),
                 (pilots.PILOT_CERTIFIED,'Practice Area',False,False,True, table2, 21),
                 (pilots.PILOT_CERTIFIED,'Cross Country',False,False,True, table2, 21),
                 (pilots.PILOT_CERTIFIED,'Pattern',      False,True, True, table2, 1),
                 (pilots.PILOT_CERTIFIED,'Practice Area',False,True, True, table2, 2),
                 (pilots.PILOT_CERTIFIED,'Cross Country',False,True, True, table2, 5),
                 (pilots.PILOT_CERTIFIED,'Pattern',      False,False,False,table2, 22),
                 (pilots.PILOT_CERTIFIED,'Practice Area',False,False,False,table2, 22),
                 (pilots.PILOT_CERTIFIED,'Cross Country',False,False,False,table2, 22),
                 (pilots.PILOT_CERTIFIED,'Pattern',      False,True, False,table2, 6),
                 (pilots.PILOT_CERTIFIED,'Practice Area',False,True, False,table2, 6),
                 (pilots.PILOT_CERTIFIED,'Cross Country',False,True, False,table2, 7),
                 (pilots.PILOT_CERTIFIED,'Pattern',      True,False,True,  table2, 3),
                 (pilots.PILOT_CERTIFIED,'Practice Area',True,False,True,  table2, 3),
                 (pilots.PILOT_CERTIFIED,'Cross Country',True,False,True,  table2, 3),
                 (pilots.PILOT_CERTIFIED,'Pattern',      True,True, True,  table2, 15),
                 (pilots.PILOT_CERTIFIED,'Practice Area',True,True, True,  table2, 16),
                 (pilots.PILOT_CERTIFIED,'Cross Country',True,True, True,  table2, 9),
                 (pilots.PILOT_CERTIFIED,'Pattern',      True,False,False, table2, 4),
                 (pilots.PILOT_CERTIFIED,'Practice Area',True,False,False, table2, 4),
                 (pilots.PILOT_CERTIFIED,'Cross Country',True,False,False, table2, 4),
                 (pilots.PILOT_CERTIFIED,'Pattern',      True,True, False, table2, 19),
                 (pilots.PILOT_CERTIFIED,'Practice Area',True,True, False, table2, 19),
                 (pilots.PILOT_CERTIFIED,'Cross Country',True,True, False, table2, 20),
                 (pilots.PILOT_50_HOURS, 'Pattern',      False,False,True, table2, 21),
                 (pilots.PILOT_50_HOURS, 'Practice Area',False,False,True, table2, 21),
                 (pilots.PILOT_50_HOURS, 'Cross Country',False,False,True, table2, 21),
                 (pilots.PILOT_50_HOURS, 'Pattern',      False,True, True, table2, 12),
                 (pilots.PILOT_50_HOURS, 'Practice Area',False,True, True, table2, 17),
                 (pilots.PILOT_50_HOURS, 'Cross Country',False,True, True, table2, 18),
                 (pilots.PILOT_50_HOURS, 'Pattern',      False,False,False,table2, 22),
                 (pilots.PILOT_50_HOURS, 'Practice Area',False,False,False,table2, 22),
                 (pilots.PILOT_50_HOURS, 'Cross Country',False,False,False,table2, 22),
                 (pilots.PILOT_50_HOURS, 'Pattern',      False,True, False,table2, 13),
                 (pilots.PILOT_50_HOURS, 'Practice Area',False,True, False,table2, 13),
                 (pilots.PILOT_50_HOURS, 'Cross Country',False,True, False,table2, 14),
                 (pilots.PILOT_50_HOURS, 'Pattern',      True,False,True,  table2, 3),
                 (pilots.PILOT_50_HOURS, 'Practice Area',True,False,True,  table2, 3),
                 (pilots.PILOT_50_HOURS, 'Cross Country',True,False,True,  table2, 3),
                 (pilots.PILOT_50_HOURS, 'Pattern',      True,True, True,  table2, 15),
                 (pilots.PILOT_50_HOURS, 'Practice Area',True,True, True,  table2, 16),
                 (pilots.PILOT_50_HOURS, 'Cross Country',True,True, True,  table2, 9),
                 (pilots.PILOT_50_HOURS, 'Pattern',      True,False,False, table2, 4),
                 (pilots.PILOT_50_HOURS, 'Practice Area',True,False,False, table2, 4),
                 (pilots.PILOT_50_HOURS, 'Cross Country',True,False,False, table2, 4),
                 (pilots.PILOT_50_HOURS, 'Pattern',      True,True, False, table2, 19),
                 (pilots.PILOT_50_HOURS, 'Practice Area',True,True, False, table2, 19),
                 (pilots.PILOT_50_HOURS, 'Cross Country',True,True, False, table2, 20)]
    for test in testcases:
        name = 'minimums' if test[5] is table1 else 'alternates'
        args = '('+','.join(map(repr,test[:-2]))+','+name+')'
        try:
            env.reset()
            mins = func(*test[:-1])
            expt = None if test[-1] is None else list(map(float,test[5][test[-1]][4:]))
            if expt != mins:
                data = (function,args,repr(mins),repr(expt))
                outp.write('%s%s returned %s, but should have returned %s.\n' % data)
                score -= 1/len(testcases)
                if not step:
                    return (FAIL_INCORRECT,max(0,score))
            if len(env.printed) != 0:
                printed = True
        except:
            import traceback
            outp.write("The call %s%s crashed.\n" % (function,args))
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


pass
#mark -
#mark Graders
def grade_module(package,module,outp=sys.stdout):
    """
    Grades the pilots package
    
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
    
    functions = [('get_certification',grade_func1),
#                 ('has_instrument_rating',grade_func2),
#                 ('has_advanced_endorsement',grade_func3),
#                 ('has_multiengine_endorsement',grade_func4),
                 ('get_best_value',grade_func5),
                 ('get_minimums',grade_func6)]
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
    return grade_module('auditor','pilots.py',outp)


if __name__ == '__main__':
    print(grade())