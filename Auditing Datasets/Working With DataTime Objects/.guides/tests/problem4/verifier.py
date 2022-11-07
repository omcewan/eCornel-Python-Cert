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


WORKSPACE = [os.path.expanduser('~'),'workspace','exercise4']


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
        funcs = load_from_path(os.path.join(*WORKSPACE,'funcs'))
        environment.capture('funcs',funcs)
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
            outp.write('There is no module docstring in %s.\n' % repr(file))
            return (FAIL_BAD_STYLE,0)
        if docs == DOCSTRING_UNCLOSED:
            outp.write('The module docstring is not properly closed.\n')
            return (FAIL_CRASHES,0.1)
        if docs == DOCSTRING_NOT_FIRST:
            outp.write('The module docstring is not the first non-blank line.\n')
            score -= 0.3
        if not step:
            return (FAIL_BAD_STYLE,max(0,score))
    docs = get_docstring(code,False)
    
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


def grade_func1(file,step=0,outp=sys.stdout):
    """
    Returns the test result and score for the implementation of str_to_time
    
    The step parameter is the phase in the grading pass.  Step 0 is a verification step
    and will stop at the first error found.  Otherwise it will continue through and try 
    to find all errors.
    
    Parameter file: The file name
    Precondition: file is a string of a file in the given workspace
    
    Parameter step: The current verfication/grading step
    Precondition: grade is 0 or 1
    
    Parameter outp: The output stream
    Precondition: outp is a stream writer
    """
    score = 1
    env = import_module(file,0)
    
    function = 'str_to_time'
    
    if type(env) == str:
        outp.write(env)
        return (FAIL_CRASHES, 0)
    elif not hasattr(env.module,function):
        outp.write("File %s is missing the header for %s.\n" % (repr(file),repr(function)))
        return (FAIL_INCORRECT, 0)
    
    # Check for try...except not present or with more than one line in the try clause STT
    tree = parse_file(file)
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
    testcases = [('2016-04-15',datetime(2016,4,15)),
                 ('October 12, 2019',datetime(2019,10,12)),
                 ('Octover 12, 2019',None),
                 ('2016-04-15T10:15:45',datetime(2016,4,15,10,15,45)),
                 ('2017-08-02 13:00:15',datetime(2017,8,2,13,0,15)),
                 ('10:15 pm, October 12, 2019',datetime(2019,10,12,22,15)),
                 ('22:15 pm, October 12, 2019',None)]
    func = getattr(env.module,function)
    printed = False
    for data in testcases:
        try:
            env.reset()
            received = func(data[0])
            expected = data[1]
            if not received is None and type(received) != datetime:
                outp.write("The call %s(%s) does not return a datetime object.\n" % (function, repr(data[0])))
                score -= 1/len(testcases)
                if not step:
                    return (FAIL_INCORRECT,max(0,score))
            if received != expected:
                outp.write("The call %s(%s) returns %s, not %s.\n" % (function, repr(data[0]), repr(received), repr(expected)))
                score -= 1/len(testcases)
                if not step:
                    return (FAIL_INCORRECT,max(0,score))
            if len(env.printed) != 0:
                printed = True
        except:
            import traceback
            outp.write("The call %s(%s) crashed.\n" % (function, repr(data[0])))
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


def grade_func2(file,step=0,outp=sys.stdout):
    """
    Returns the test result and score for the implementation of sunset
    
    The step parameter is the phase in the grading pass.  Step 0 is a verification step
    and will stop at the first error found.  Otherwise it will continue through and try 
    to find all errors.
    
    Parameter file: The file name
    Precondition: file is a string of a file in the given workspace
    
    Parameter step: The current verfication/grading step
    Precondition: grade is 0 or 1
    
    Parameter outp: The output stream
    Precondition: outp is a stream writer
    """
    score = 1
    env = import_module(file,0)
    
    function = 'sunset'
    
    if type(env) == str:
        outp.write(env)
        return (FAIL_CRASHES, 0)
    elif not hasattr(env.module,function):
        outp.write("File %s is missing the header for %s.\n" % (repr(file),repr(function)))
        return (FAIL_INCORRECT, 0)
    
    filepath = os.path.join(*WORKSPACE,'daycycle.json')
    file = open(filepath)
    daycycle = json.loads(file.read())
    file.close()
    
    from datetime import date, datetime
    testcases = [(date(2017,8,2),datetime(2017,8,2,19,24)),
                 (date(2019,12,25),datetime(2019,12,25,16,38)),
                 (date(2016,6,2),datetime(2016,6,2,19,38)),
                 (date(2016,12,25),datetime(2016,12,25,16,39)),
                 (date(2014,6,2),None),
                 (date(2022,12,25),None)]
    func = getattr(env.module,function)
    printed = False
    for data in testcases:
        try:
            env.reset()
            received = func(data[0],daycycle)
            expected = data[1]
            if not received is None and type(received) != datetime:
                outp.write("The call %s(%s,%s) does not return a datetime object.\n" % (function, repr(data[0]), 'daycycle'))
                score -= 1/len(testcases)
                if not step:
                    return (FAIL_INCORRECT,max(0,score))
            if received != expected:
                outp.write("The call %s(%s,%s) returns %s, not %s.\n" % (function, repr(data[0]), 'daycycle', repr(received), repr(expected)))
                score -= 1/len(testcases)
                if not step:
                    return (FAIL_INCORRECT,max(0,score))
            if len(env.printed) != 0:
                printed = True
        except:
            import traceback
            outp.write("The call %s(%s,%s) crashed.\n" % (function, repr(data[0]), 'daycycle'))
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
def grade_file(file,outp=sys.stdout):
    """
    Grades the two functions
    
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
    crashes = status
    
    func = 'str_to_time'
    if not crashes:
        outp.write("Comments for %s:\n" % repr(func))
        status, p2 = grade_func1(file,1,outp)
        if p2 == 1:
            outp.write('The function looks good.\n\n')
        else:
            outp.write('\n')
    else:
        p2 = 0
    
    func = 'sunset'
    if not crashes:
        outp.write("Comments for %s:\n" % repr(func))
        status, p3 = grade_func2(file,1,outp)
        if p3 == 1:
            outp.write('The function looks good.\n\n')
        else:
            outp.write('\n')
    else:
        p3 = 0
    
    total = round(0.05*p1+0.5*p2+0.45*p3,3)
    return total


def grade(outp=sys.stdout):
    """
    Invokes this subgrader (returning a percentage)
    """
    return grade_file('funcs.py',outp)


if __name__ == '__main__':
    print(grade())