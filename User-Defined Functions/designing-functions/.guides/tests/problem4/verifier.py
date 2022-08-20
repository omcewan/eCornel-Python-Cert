"""
The verification functions for Course 2 scripts

This file is insecurely available to students, but if they find it and modify it, they
really did not need this course.

Author: Walker M. White
Date:   July 31, 2018
"""
import os, os.path, sys
import importlib, importlib.util
import traceback
import inspect
import builtins
import ast
from modlib import Environment

# For support
import introcs

#mark Constants

# The status codes
TEST_SUCCESS      = 0
FAIL_NO_FILE      = 1
FAIL_BAD_STYLE    = 2
FAIL_CRASHES      = 4
FAIL_INCORRECT    = 5


WORKSPACE = [os.path.expanduser('~'),'workspace','exercise4']
#WORKSPACE = []


DOCSTRING = """
    Returns: The initials <first>. <last>. of the given name.
    
    We assume that n is just two names (first and last). Middle names are
    not supported.
    
    Example: initials('John Smith') returns 'J. S.'
    Example: initials('Walker White') returns 'W. W.'
    
    Parameter n: the person's name
    Precondition: n is in the form 'first-name last-name' with one space between names.
    There are no spaces in either <first-name> or <last-name>
    """

#mark -
#mark Helpers
def read_file(name):
    """
    Returns the contents of the file or None if missing.
    
    Parameter name: The file name
    Precondition: name is a string
    """
    path = os.path.join(*WORKSPACE,name)
    try:
        with open(path) as file:
            result = file.read()
        return result
    except:
        return None


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


def import_module(name,step=0):
    """
    Returns a reference to the module.
    
    Returns an error message if it fails.
    
    Parameter name: The module name
    Precondition: name is a string
    """
    try:
        import types
        refs = os.path.splitext(name)[0]
        environment = Environment(refs,WORKSPACE)
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
        return (msg,None)


# Localized error codes
DOCSTRING_MISSING   = 1
DOCSTRING_UNCLOSED  = 2
DOCSTRING_NOT_FIRST = 3

def get_docstring(text,first=True):
    """
    Returns the docstring as a list of lines
    
    This function returns an error code if there is no initial docstring.
    
    Parameter text: The text to search for a docstring.
    Precondition: text is a string
    
    Parameter text: Whether to require the docstring to be first.
    Precondition: text is a string
    """
    lines = text.split('\n')
    lines = list(map(lambda x: x.strip(),lines))
    
    start = -1
    for pos in range(len(lines)):
        if len(lines[pos]) >= 3 and lines[pos][:3] in ['"""',"'''"]:
            start = pos
            break
    
    if start == -1:
        return DOCSTRING_MISSING
    
    end = -1
    for pos in range(start+1,len(lines)):
        if lines[pos][-3:] == lines[start][:3]:
            end = pos
            break
    
    if end == -1:
        return DOCSTRING_UNCLOSED
    
    if first:
        for pos in range(start):
            if len(lines[pos]) > 0:
                return DOCSTRING_NOT_FIRST
    
    # One last trim
    if len(lines[start]) > 3:
        lines[start] = lines[start][3:]
    else:
        start += 1
    if len(lines[end]) > 3:
        lines[end] = lines[end][:-3]
    else:
        end -= 1
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
def grade_docstring(file,step=0,outp=sys.stdout):
    """
    Returns the test result and score for the docstring.
    
    The step parameter is the phase in the grading pass.  Step 0 is a verification step
    and will stop at the first error found.  Otherwise it will continue through and try 
    to find all errors.
    
    Parameter name: The file name
    Precondition: name is a string of a file in the given workspace
    
    Parameter step: The current verfication/grading step
    Precondition: grade is 0 or 1
    
    Parameter outp: The output stream
    Precondition: outp is a stream writer
    """
    code = read_file(file)
    if code is None:
        outp.write('Could not find the file %s.\n' % repr(file))
        return (FAIL_NO_FILE, 0)
    
    score = 1
    docs = get_docstring(code)
    if type(docs) == int:
        if docs == DOCSTRING_MISSING:
            outp.write('There is no docstring in %s.\n' % repr(file))
            return (FAIL_BAD_STYLE,0)
        if docs == DOCSTRING_UNCLOSED:
            outp.write('The docstring is not properly closed.\n')
            return (FAIL_CRASHES,0.1)
        if docs == DOCSTRING_NOT_FIRST:
            outp.write('The docstring is not the first non-blank line.\n')
            score -= 0.3
        if not step:
            return (FAIL_BAD_STYLE,max(0,score))
    docs = get_docstring(code,False)
    
    test = check_name(docs)
    if test:
        if test == NAME_MISSING:
            outp.write("The second-to-last line in the docstring does not start with 'Author:'\n")
            score -= 0.3
        if test == NAME_INCOMPLETE:
            outp.write("There is no name after 'Author:'\n")
            score -= 0.1
        if not step:
            return (FAIL_BAD_STYLE,max(0,score))
    test = check_date(docs)
    if test:
        if test == DATE_MISSING:
            outp.write("The last line in the docstring does not start with 'Date:'\n")
            score -= 0.2
        if test == DATE_INCOMPLETE:
            outp.write("The date after 'Date:' is invalid.\n")
            score -= 0.1
        if not step:
            return (FAIL_BAD_STYLE, max(0,score))
    
    return (TEST_SUCCESS, max(0,score))


def grade_get_seconds(file,step=0,outp=sys.stdout):
    """
    Returns the test result and score for the helper get_seconds.
    
    The step parameter is the phase in the grading pass.  Step 0 is a verification step
    and will stop at the first error found.  Otherwise it will continue through and try 
    to find all errors.
    
    Parameter name: The file name
    Precondition: name is a string of a file in the given workspace
    
    Parameter step: The current verfication/grading step
    Precondition: grade is 0 or 1
    
    Parameter outp: The output stream
    Precondition: outp is a stream writer
    """
    env = import_module(file)
    if type(env) == str:
        outp.write(env)
        return (FAIL_CRASHES,0)
    elif not hasattr(env.module,'get_seconds'):
        outp.write("File %s is missing the header for 'get_seconds'.\n" % repr(file))
        return (FAIL_INCORRECT,0)
    
    score = 1
    func = env.module.get_seconds
    if func.__doc__ is None:
        outp.write("The docstring for 'get_seconds' is missing.\n")
        score -= 0.1
        if not step:
            return (FAIL_BAD_STYLE,max(0,score))
    
    tests = [('12:35:15',15),('03:02:05',5),('00:00:00',0),('23:59:59',59),('11:10:09',9)]
    once = True
    for pair in tests:
        try:
            if func(pair[0]) != pair[1]:
                outp.write("The call get_seconds(%s) returned %s and not %s.\n" % (repr(pair[0]),repr(func(pair[0])),repr(pair[1])))
                if once and func(pair[0]) == str(pair[1]):
                    output.write("Remember to convert your final answer to an int.\n")
                    once = False
                score -= 0.2
                if not step:
                    return (FAIL_INCORRECT,max(0,score))
        except:
            import traceback
            outp.write("The function 'get_seconds' crashed on valid input time=%s.\n" % repr(pair[0]))
            outp.write(traceback.format_exc(0))
            score -= 0.2
            if not step:
                return (FAIL_INCORRECT,max(0,score))
    
    if len(env.printed):
        outp.write("The function 'get_seconds' contains print statements.\n")
        score -= 0.2
        if not step:
            return (FAIL_BAD_STYLE,max(0,score))
    
    return (TEST_SUCCESS,max(0,score))


def grade_get_minutes(file,step=0,outp=sys.stdout):
    """
    Returns the test result and score for the helper get_minutes.
    
    The step parameter is the phase in the grading pass.  Step 0 is a verification step
    and will stop at the first error found.  Otherwise it will continue through and try 
    to find all errors.
    
    Parameter name: The file name
    Precondition: name is a string of a file in the given workspace
    
    Parameter step: The current verfication/grading step
    Precondition: grade is 0 or 1
    
    Parameter outp: The output stream
    Precondition: outp is a stream writer
    """
    env = import_module(file)
    if type(env) == str:
        outp.write(env)
        return (FAIL_CRASHES,0)
    elif not hasattr(env.module,'get_minutes'):
        outp.write("File %s is missing the header for 'get_minutes'.\n" % repr(file))
        return (FAIL_INCORRECT,0)
    
    score = 1
    func = env.module.get_minutes
    if func.__doc__ is None:
        outp.write("The docstring for 'get_minutes' is missing.\n")
        score -= 0.1
        if not step:
            return (FAIL_BAD_STYLE,max(0,score))
    
    tests = [('12:35:15',35),('03:02:05',2),('00:00:00',0),('23:59:59',59),('11:09:10',9)]
    once = True
    for pair in tests:
        try:
            if func(pair[0]) != pair[1]:
                outp.write("The call get_minutes(%s) returned %s and not %s.\n" % (repr(pair[0]),repr(func(pair[0])),repr(pair[1])))
                if once and func(pair[0]) == str(pair[1]):
                    output.write("Remember to convert your final answer to an int.\n")
                    once = False
                score -= 0.2
                if not step:
                    return (FAIL_INCORRECT,max(0,score))
        except:
            import traceback
            outp.write("The function 'get_minutes' crashed on valid input time=%s.\n" % repr(pair[0]))
            outp.write(traceback.format_exc(0))
            score -= 0.2
            if not step:
                return (FAIL_INCORRECT,max(0,score))
    
    if len(env.printed):
        outp.write("The function 'get_minutes' contains print statements.\n")
        score -= 0.2
        if not step:
            return (FAIL_BAD_STYLE,max(0,score))
    
    return (TEST_SUCCESS,max(0,score))


def grade_get_hours(file,step=0,outp=sys.stdout):
    """
    Returns the test result and score for the helper get_hours.
    
    The step parameter is the phase in the grading pass.  Step 0 is a verification step
    and will stop at the first error found.  Otherwise it will continue through and try 
    to find all errors.
    
    Parameter name: The file name
    Precondition: name is a string of a file in the given workspace
    
    Parameter step: The current verfication/grading step
    Precondition: grade is 0 or 1
    
    Parameter outp: The output stream
    Precondition: outp is a stream writer
    """
    env = import_module(file)
    if type(env) == str:
        outp.write(env)
        return (FAIL_CRASHES,0)
    elif not hasattr(env.module,'get_hours'):
        outp.write("File %s is missing the header for 'get_hours'.\n" % repr(file))
        return (FAIL_INCORRECT,0)
    
    score = 1
    func = env.module.get_hours
    if func.__doc__ is None:
        outp.write("The docstring for 'get_hours' is missing.\n")
        score -= 0.1
        if not step:
            return (FAIL_BAD_STYLE,max(0,score))
    
    tests = [('12:35:15',12),('03:02:05',3),('00:00:00',0),('23:59:59',23),('09:11:10',9)]
    once = True
    for pair in tests:
        try:
            if func(pair[0]) != pair[1]:
                outp.write("The call get_hours(%s) returned %s and not %s.\n" % (repr(pair[0]),repr(func(pair[0])),repr(pair[1])))
                if once and func(pair[0]) == str(pair[1]):
                    output.write("Remember to convert your final answer to an int.\n")
                    once = False
                score -= 0.2
                if not step:
                    return (FAIL_INCORRECT,max(0,score))
        except:
            import traceback
            outp.write("The function 'get_hours' crashed on valid input time=%s.\n" % repr(pair[0]))
            outp.write(traceback.format_exc(0))
            score -= 0.2
            if not step:
                return (FAIL_INCORRECT,max(0,score))
    
    if len(env.printed):
        outp.write("The function 'get_hours' contains print statements.\n")
        score -= 0.2
        if not step:
            return (FAIL_BAD_STYLE,max(0,score))
    
    return (TEST_SUCCESS,max(0,score))


def grade_str_to_seconds(file,step=0,outp=sys.stdout):
    """
    Returns the test result and score for the helper get_hours.
    
    The step parameter is the phase in the grading pass.  Step 0 is a verification step
    and will stop at the first error found.  Otherwise it will continue through and try 
    to find all errors.
    
    Parameter name: The file name
    Precondition: name is a string of a file in the given workspace
    
    Parameter step: The current verfication/grading step
    Precondition: grade is 0 or 1
    
    Parameter outp: The output stream
    Precondition: outp is a stream writer
    """
    env = import_module(file)
    if type(env) == str:
        outp.write(env)
        return (FAIL_CRASHES,0)
    elif not hasattr(env.module,'str_to_seconds'):
        outp.write("File %s is missing the header for 'str_to_seconds'.\n" % repr(file))
        return (FAIL_INCORRECT,0)
    
    score = 1
    func = env.module.str_to_seconds
    if func.__doc__ is None:
        outp.write("The docstring for 'str_to_seconds' is missing.\n")
        score -= 0.1
        if not step:
            return (FAIL_INCORRECT,max(0,score))
    
    tests = [('00:00:00',0),('00:00:59',59),('00:01:00',60),('01:00:00',3600),('01:01:00',3660),
             ('01:01:01',3661),('12:35:15',45315),('03:02:05',10925),('23:59:59',86399),
             ('02:02:02',7322)]
    for pair in tests:
        try:
            if func(pair[0]) != pair[1]:
                outp.write("The call str_to_seconds(%s) returned %s and not %s.\n" % (repr(pair[0]),repr(func(pair[0])),repr(pair[1])))
                score -= 0.2
                if not step:
                    return (FAIL_INCORRECT,max(0,score))
        except:
            import traceback
            outp.write("The function 'str_to_seconds' crashed on valid input time=%s.\n" % repr(pair[0]))
            outp.write(traceback.format_exc(0))
            score -= 0.2
            if not step:
                return (FAIL_INCORRECT,max(0,score))
    
    if len(env.printed):
        outp.write("The function 'str_to_seconds' contains print statements.\n")
        score -= 0.2
        if not step:
            return (FAIL_BAD_STYLE,max(0,score))
    
    # Now for some code inspection
    code = parse_file(file)
    body = None
    for item in code.body:
        if type(item) == ast.FunctionDef and item.name == 'str_to_seconds':
            body = item.body
    
    check = {'get_seconds':0,'get_minutes':0,'get_hours':0}
    for line in body:
        for item in ast.walk(line):
            if type(item) == ast.Call:
                if item.func.id in check:
                    check[item.func.id] = 1
    
    if sum(check.values()) != 3:
        bad = list(map(lambda x : x[0], filter(lambda x: x[1] == 0, check.items())))
        outp.write("Function 'str_to_seconds' did not call the following helpers: ")
        outp.write(', '.join(bad)+'.\n')
        score -= 0.2
        if not step:
            return (FAIL_INCORRECT,max(0,score))
    
    return (TEST_SUCCESS,max(0,score))


pass
#mark -
#mark Graders
def grade_file(file,outp=sys.stdout):
    """
    Grades the interactive script, weighting earlier parts less.
    
    Parameter name: The file name
    Precondition: name is a string
    
    Parameter outp: The output stream
    Precondition: outp is a stream writer
    """
    outp.write('Docstring comments:\n')
    status, p1 = grade_docstring(file,1,outp)
    if p1 == 1:
        outp.write('The module docstring looks good.\n\n')
    else:
        outp.write('\n')
    
    if not status:
        outp.write('get_seconds comments:\n')
        status, p2 = grade_get_seconds(file,1,outp)
        if p2 == 1:
            outp.write('The function get_seconds looks good.\n\n')
        else:
            outp.write('\n')
    else:
        p2 = 0
    
    if not status:
        outp.write('get_minutes comments:\n')
        status, p3 = grade_get_minutes(file,1,outp)
        if p3 == 1:
            outp.write('The function get_minutes looks good.\n\n')
        else:
            outp.write('\n')
    else:
        p3 = 0
    
    if not status:
        outp.write('get_hours comments:\n')
        status, p4 = grade_get_hours(file,1,outp)
        if p4 == 1:
            outp.write('The function get_hours looks good.\n\n')
        else:
            outp.write('\n')
    else:
        p4 = 0
    
    if not status:
        outp.write('str_to_seconds comments:\n')
        status, p5 = grade_str_to_seconds(file,1,outp)
        if p5 == 1:
            outp.write('The function str_to_seconds looks good.\n\n')
        else:
            outp.write('\n')
    else:
        p5 = 0
    
    total = round(0.05*p1+0.2*p2+0.2*p3+0.2*p4+0.35*p5,3)
    return total


def grade(outp=sys.stdout):
    """
    Invokes this subgrader (returning a percentage)
    """
    return grade_file('funcs.py',outp)


if __name__ == '__main__':
    print(grade())