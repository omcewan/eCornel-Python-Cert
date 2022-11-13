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


def build_hours(utils):
    """
    Returns a 2d list of plane hours by date (used for error messages).
    
    The date is in the format
        
        PLANE TIMEIN TIMEOUT HOURS
    
    Each entry can represent a flight, or a repair.  Normal repairs
    have a -1 for hours while annuals have a -2 for repairs.  Flights
    have the total hours flown for that flight.
    
    This data is sorted by timein, allowing us to quickly look-up 
    when producing error messages.
    
    Parmeter utils: The utils module to use
    Precondition: utils is a loaded instance of the utils module
    """
    import datetime
    dataset = []
    
    parent = os.path.join(*TESTFILES)    
    fpath  = os.path.join(parent,'repairs.csv')
    for item in utils.read_csv(fpath)[1:]:
        start = utils.str_to_time(item[1])
        ends  = utils.str_to_time(item[2])
        type  = -2 if item[3] == 'annual inspection' else -1
        dataset.append([item[0],start,ends,type])
    
    fpath  = os.path.join(parent,'lessons.csv')
    for item in utils.read_csv(fpath)[1:]:
        start = utils.str_to_time(item[3]).replace(tzinfo=None)
        ends  = utils.str_to_time(item[4]).replace(tzinfo=None)
        hours = round((ends-start).seconds/(60*60))
        dataset.append([item[1],start,ends,hours])
    
    fpath  = os.path.join(parent,'fleet.csv')
    for item in utils.read_csv(fpath)[1:]:
        start = utils.str_to_time(item[5])
        end   = start+datetime.timedelta(seconds=1)
        hours = int(item[6])
        dataset.append([item[0],start,start,-2]) # Record annual    
        dataset.append([item[0],end,end,hours])  # Record carry over hours
    
    dataset.sort(key=lambda x:x[1])
    return dataset


def get_hours(plane,timestamp,hourset,utils):
    """
    Returns the number of hours plane has flown BEFORE timestamp
    
    The number returned does not include the flight at timestamp (assuming
    it is a flight).
    
    Parameter plane: The id of a plane
    Precondition: plane is a string
    
    Parameter timestamp: The time to query
    Precondition: timestamp is a str representing a date in iso format
    
    Parameter hourset: The database of plane hours
    Precondition: hourset is 2d list created by build_hours()
    
    
    Parmeter utils: The utils module to use
    Precondition: utils is a loaded instance of the utils module
    """
    date = utils.str_to_time(timestamp).replace(tzinfo=None)
    hours = 0
    pos = 0
    while pos < len(hourset):
        curr = hourset[pos]
        pos += 1
        if curr[0] == plane:
            if curr[1] < date:
                if curr[3] >= 0:
                    hours += curr[3]
                else:
                    hours = 0
            else:
                pos = len(hourset)
    return hours


def get_annual(plane,timestamp,hourset,utils):
    """
    Returns the most recent annual for this plane BEFORE timestamp
    
    The value returned is actually (annual,days) where annual is date
    object (not a datetime object) and days is the number of days between
    timestamps and annual.
    
    Parameter plane: The id of a plane
    Precondition: plane is a string
    
    Parameter timestamp: The time to query
    Precondition: timestamp is a str representing a date in iso format
    
    Parameter hourset: The database of plane hours
    Precondition: hourset is 2d list created by build_hours()
    
    Parmeter utils: The utils module to use
    Precondition: utils is a loaded instance of the utils module
    """
    date = utils.str_to_time(timestamp).replace(tzinfo=None)
    pos = 0
    annual = None
    while pos < len(hourset):
        curr = hourset[pos]
        pos += 1
        if curr[0] == plane and curr[3] == -2:
            if annual is None:
                annual = curr[1]
            elif curr[1] >= date:
                pos = len(hourset)
            elif annual < curr[1]:
                annual = curr[1]
    
    days = (date-annual).days
    return (annual.date(),days)


def get_repairs(plane,timestamp,hourset,utils):
    """
    Returns the most recent repair for this plane that began BEFORE timestamp
    
    The value returned is actually (timein,timeout) where timein and timeout
    are both date objects (not a datetime objects).
    
    Parameter plane: The id of a plane
    Precondition: plane is a string
    
    Parameter timestamp: The time to query
    Precondition: timestamp is a str representing a date in iso format
    
    Parameter hourset: The database of plane hours
    Precondition: hourset is 2d list created by build_hours()
    
    Parmeter utils: The utils module to use
    Precondition: utils is a loaded instance of the utils module
    """
    date = utils.str_to_time(timestamp).replace(tzinfo=None)
    pos = 0
    timein  = None
    timeout = None
    while pos < len(hourset):
        curr = hourset[pos]
        pos += 1
        if curr[0] == plane and curr[3] < 0:
            if timein is None:
                timein  = curr[1]
                timeout = curr[2]
            elif curr[1] >= date:
                pos = len(hourset)
            elif timein < curr[1]:
                timein  = curr[1]
                timeout = curr[2]
    
    return (timein.date(),timeout.date())


def false_negative(utils, flight,hourset,reason=None):
    """
    Returns a message explaining a false negative result.
    
    Parmeter utils: The utils module to use
    Precondition: utils is a loaded instance of the utils module
    
    Parameter flight: The flight that should have been detected
    Precondition: flight is a row in the correct list of answers
    
    Parameter hourset: The database of plane hours
    Precondition: hourset is 2d list created by build_hours()
    
    Parameter reason: The (incorrect) reason given (or None if missed)
    Precondition: reason is None or one of 'Inspection', 'Annual', 'Grounded', 'Maintenance'
    """
    message = None
    if reason == 'Maintenance' or flight[-1] == 'Maintenance':
        hours = get_hours(flight[1],flight[3],hourset,utils)
        start = utils.str_to_time(flight[3]).replace(tzinfo=None)
        stop  = utils.str_to_time(flight[4]).replace(tzinfo=None)
        hours += (stop-start).seconds/(60*60)
        plural1 = 's' if hours != 1 else ''
        timein, timeout = get_repairs(flight[1],flight[3],hourset,utils)
        annual, days = get_annual(flight[1],flight[3],hourset,utils)
        plural2 = 's' if days != 1 else ''
        data = (flight[1],flight[4],hours,plural1,timeout.isoformat(),days,plural2,annual.isoformat())
        message = 'Plane %s landed on %s with %s hour%s since its last repair on %s and %s day%s since its last annual on %s.' % data
    elif flight[-1] == 'Inspection':
        hours = get_hours(flight[1],flight[3],hourset,utils)
        start = utils.str_to_time(flight[3]).replace(tzinfo=None)
        stop  = utils.str_to_time(flight[4]).replace(tzinfo=None)
        hours += (stop-start).seconds/(60*60)
        plural = 's' if hours != 1 else ''
        data  = (flight[1],hours,plural,flight[3])
        message = 'Plane %s had %d hour%s after the flight at %s.' % data
    elif flight[-1] == 'Annual':
        annual, days = get_annual(flight[1],flight[3],hourset,utils)
        plural = 's' if days != 1 else ''
        data = (flight[1],annual.isoformat(),repr(days),plural,flight[3])
        message = 'Plane %s last had an annual inspection on %s, %s day%s before %s.' % data
    elif flight[-1] == 'Grounded':
        timein, timeout = get_repairs(flight[1],flight[3],hourset,utils)
        data = (flight[1],timein.isoformat(),timeout.isoformat(),flight[3])
        message = 'Plane %s was in maintenance between %s and %s, overlapping the flight at %s.' % data
    return message


def false_positive(utils,flight,hourset):
    """
    Returns a message explaining a false positive result.
    
    Parmeter utils: The utils module to use
    Precondition: utils is a loaded instance of the utils module
    
    Parameter flight: The flight that should have been detected
    Precondition: flight is a row in the correct list of answers
    
    Parameter hourset: The database of plane hours
    Precondition: hourset is 2d list created by build_hours()
    """
    message = None
    if flight[-1] == 'Inspection':
        hours = get_hours(flight[1],flight[3],hourset,utils)
        start = utils.str_to_time(flight[3]).replace(tzinfo=None)
        stop  = utils.str_to_time(flight[4]).replace(tzinfo=None)
        hours += (stop-start).seconds/(60*60)
        explain = 'had exactly' if hours == 100 else 'only had'
        plural = 's' if hours != 1 else ''
        data  = (flight[1],explain,hours,plural,flight[3])
        message = 'Plane %s %s %d hour%s after the flight at %s.' % data
    elif flight[-1] == 'Annual':
        annual, days = get_annual(flight[1],flight[3],hourset,utils)
        plural = 's' if days != 1 else ''
        data = (flight[1],annual.isoformat(),repr(days),plural,flight[3])
        message = 'Plane %s had an annual inspection on %s, %s day%s before %s.' % data
    elif flight[-1] == 'Grounded':
        timein, timeout = get_repairs(flight[1],flight[3],hourset,utils)
        data = (flight[1],timeout.isoformat(),flight[3])
        message = 'Plane %s was last in maintenance on %s before the flight at %s.' % data
    else: # Maintenance
        hours = get_hours(flight[1],flight[3],hourset,utils)
        start = utils.str_to_time(flight[3]).replace(tzinfo=None)
        stop  = utils.str_to_time(flight[4]).replace(tzinfo=None)
        hours += (stop-start).seconds/(60*60)
        plural1 = 's' if hours != 1 else ''
        timein, timeout = get_repairs(flight[1],flight[3],hourset,utils)
        annual, days = get_annual(flight[1],flight[3],hourset,utils)
        plural2 = 's' if days != 1 else ''
        data = (flight[1],flight[4],hours,plural1,timeout.isoformat(),days,plural2,annual.isoformat())
        message = 'Plane %s landed on %s with %s hour%s since its last repair on %s and %s day%s since its last annual on %s.' % data
    return message


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
    Returns the test result and score for the implementation of list_inspection_violations
    
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
    function = 'list_inspection_violations'
    
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
    fpath   = os.path.join(*TESTFILES,'badplanes.csv')
    correct = utils.read_csv(fpath)[1:]
    
    # Lets construct a dataset for better feedback
    hourset = build_hours(utils)
    
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
            message = '%s(%s) is missing the flight %s for pilot %s' % data
            message += '\n'+false_negative(utils,correct[key],hourset)+'\n'
            outp.write(message)
            score -= 0.05
            if not step:
                return (FAIL_INCORRECT,max(0,score))
    
    for key in results:
        if not key in correct:
            data = (function,repr(tdir),results[key][3],results[key][0])
            message = '%s(%s) identified flight %s for pilot %s, even though it is okay' % data
            message += '\n'+false_positive(utils,results[key],hourset)+'\n'
            outp.write(message)
            score -= 0.05
            if not step:
                return (FAIL_INCORRECT,max(0,score))
    
    for key in correct:
        if key in results and (correct[key][-1] != results[key][-1]):
            data = (function,repr(tdir),correct[key][3],correct[key][0],
                    repr(results[key][-1]),repr(correct[key][-1]))
            message = "%s(%s) identified flight %s for pilot %s as %s, not %s" % data
            message += '\n'+false_negative(utils,correct[key],hourset,results[key][-1])+'\n'
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
    
    functions = [('list_inspection_violations',grade_func1)]
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
    return grade_module('auditor','inspections.py',outp)


if __name__ == '__main__':
    print(grade())