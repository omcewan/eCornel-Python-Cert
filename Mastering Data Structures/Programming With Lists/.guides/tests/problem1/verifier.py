"""
The verification functions for Course 4 scripts

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
import copy
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


WORKSPACE = [os.path.expanduser('~'),'workspace','exercise1']
#WORKSPACE = []


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


def import_module(name,base=0):
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
#mark Fold Functions
# Some f values to test
def add(x,y):
    """
    Returns the sum x+y
    
    This works on any types that support addition (numbers, strings, etc.)
    
    Parameter x: The first value to add
    Precondition: x supports addition and x is same type as y
    
    Parameter x: The second value to add
    Precondition: x supports addition and x is same type as y
    """
    return x+y


def sub(x,y):
    """
    Returns the difference x-y
    
    Parameter x: The value to subtract from
    Precondition: x is a number
    
    Parameter y: The value to subtract
    Precondition: y is a number
    """
    return x-y


def remove(s1,s2):
    """
    Returns a copy of s, with all characters in s2 removed.
    
    Examples:
        remove('abc','ab') returns 'c'
        remove('abc','xy') returns 'abc'
        remove('hello world','ol') returns 'he wrd'
    
    Parameter s1: the string to copy
    Precondition: s1 is a string
    
    Parameter s2: the characters to remove
    Precondition: s2 is a string
    """
    result = ''
    for x in s1:
        if not x in s2:
            result = result + x
    return result


def duplicate(s1,s2):
    """
    Returns a copy of s, with all characters in s2 duplicated.
    
    Examples:
        duplicate('abc','ab') returns 'aabbbc'
        duplicate('abc','xy') returns 'abc'
        duplicate('hello world','ol') returns 'helllloo woolld'
    
    Parameter s1: the string to copy
    Precondition: s1 is a string
    
    Parameter s2: the characters to remove
    Precondition: s2 is a string
    """
    chars = set(s2)
    result = s1
    for x in chars:
        result = result.replace(x,x+x)
    return result


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
    Returns the test result and score for the implementation of add_time1
    
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
    
    function = 'put_in'
    
    if type(env) == str:
        outp.write(env)
        return (FAIL_CRASHES, 0)
    elif not hasattr(env.module,function):
        outp.write("File %s is missing the header for %s.\n" % (repr(file),repr(function)))
        return (FAIL_INCORRECT, 0)
    
    
    testcase = [([0,1,2,4],3,[0,1,2,3,4]),
                ([0,1,2,3,4],-1,[-1,0,1,2,3,4]),
                ([-1,0,1,2,3,4],2,[-1,0,1,2,2,3,4]),
                ([-1,0,1,2,2,3,4],0,[-1,0,0,1,2,2,3,4]),
                (['a','aa','ab','b','ce'],'aab',['a','aa','aab','ab','b','ce']),
                (['a','aa','ab','b','ce'],'aab',['a','aa','aab','ab','b','ce']),
                ([(0,0),(1,0),(1,1)],(0,1),[(0,0),(0,1),(1,0),(1,1)]),
                ([],0,[0]),([0],1,[0,1])]
    
    func = getattr(env.module,function)
    printed = False
    for data in testcase:
        args = data[:-1]
        brgs = copy.deepcopy(args)
        alst = args[0]
        expected = data[-1]
        try:
            env.reset()
            received = func(*args)
            if not received is None:
                outp.write("The call %s%s returns %s, not None.\n" % (function, repr(brgs), repr(received)))
                score -= 1/len(testcase)
                if not step:
                    return (FAIL_INCORRECT,max(0,score))
            elif alst != expected and alst == brgs[0]:
                outp.write("The call %s%s did not modify the list.\n" % (function, repr(brgs)))
                score -= 1/len(testcase)
                if not step:
                    return (FAIL_INCORRECT,max(0,score))
            elif alst != expected:
                outp.write("The call %s%s modified the list to %s when %s was expected.\n" % (function, repr(brgs), repr(alst), repr(expected)))
                score -= 1/len(testcase)
                if not step:
                    return (FAIL_INCORRECT,max(0,score))
            if len(env.printed) != 0:
                printed = True
        except:
            import traceback
            outp.write("The call %s%s crashed.\n" % (function, repr(brgs)))
            outp.write(traceback.format_exc()+'\n')
            score -= 1/len(testcase)
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
    Returns the test result and score for the implementation of add_time2
    
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
    env = import_module(file)
    
    function = 'rotate'
    
    if type(env) == str:
        outp.write(env)
        return (FAIL_CRASHES, 0)
    elif not hasattr(env.module,function):
        outp.write("File %s is missing the header for %s.\n" % (repr(file),repr(function)))
        return (FAIL_INCORRECT, 0)
    
    testcase = [([0,1,3,5],[5,0,1,3]),([5,0,1,3],[3,5,0,1]),([3,5,0,1],[1,3,5,0]),
                ([1,3,5,0],[0,1,3,5]),(['a','b','c','d'],['d','a','b','c']),([9],[9])]
    
    func = getattr(env.module,function)
    printed = False
    for data in testcase:
        args = data[0]
        brgs = args[:]
        expected = data[1]
        try:
            env.reset()
            received = func(args)
            if not received is None:
                outp.write("The call %s(%s) returns %s, not None.\n" % (function, repr(brgs), repr(received)))
                score -= 1/len(testcase)
                if not step:
                    return (FAIL_INCORRECT,max(0,score))
            elif args != expected and args == brgs:
                outp.write("The call %s(%s) did not modify the list.\n" % (function, repr(brgs)))
                score -= 1/len(testcase)
                if not step:
                    return (FAIL_INCORRECT,max(0,score))
            elif args != expected:
                outp.write("The call %s(%s) modified the list to %s when %s was expected.\n" % (function, repr(brgs), repr(args), repr(expected)))
                score -= 1/len(testcase)
                if not step:
                    return (FAIL_INCORRECT,max(0,score))
            if len(env.printed) != 0:
                printed = True
        except:
            import traceback
            outp.write("The call %s(%s) crashed.\n" % (function, repr(brgs)))
            outp.write(traceback.format_exc()+'\n')
            score -= 1/len(testcase)
            if not step:
                return (FAIL_INCORRECT,max(0,score))
    
    if printed:
        outp.write("You must remove all debugging print statements from %s.\n" % repr(function))
        score -= 0.1
        if not step:
            return (FAIL_BAD_STYLE,max(0,score))
    
    return (TEST_SUCCESS,max(0,score))


def grade_structure(file,func,step=0,outp=sys.stdout):
    """
    Returns the test result and score for the proper control structures.
    
    The step parameter is the phase in the grading pass.  Step 0 is a verification step
    and will stop at the first error found.  Otherwise it will continue through and try 
    to find all errors.
    
    Parameter file: The file name
    Precondition: file is a string of a file in the given workspace

    Parameter file: The function name
    Precondition: file is a string
    
    Parameter step: The current verfication/grading step
    Precondition: grade is 0 or 1
    
    Parameter outp: The output stream
    Precondition: outp is a stream writer
    """
    score = 1
    code = parse_file(file)
    if type(code) == str:
        outp.write('There was a problem reading file %s.\n' % repr(file))
        outp.write(code+'\n')
        return (FAIL_NO_FILE, 0)
    
    # Find the function body
    body = None
    for item in code.body:
        if type(item) == ast.FunctionDef and item.name == func:
            body = item
    
    if body is None:
        outp.write("File %s is missing the definition for %s.\n" % (repr(file),repr(func)))
        return (FAIL_INCORRECT, 0)
    
    found1 = False
    found2 = False
    found3 = False
    for item in ast.walk(body):
        if type(item) == ast.For:
            found1 = True
        elif type(item) == ast.While:
            found2 = True
        elif type(item) == ast.Call and type(item.func) == ast.Name and item.func.id == func:
            found3 = True
    
    if found2:
        outp.write('Function %s uses a while-loop, which is not allowed.\n' % repr(func))
        score -= 0.5
        if not step:
            return (FAIL_INCORRECT,max(0,score))
    elif found1:
        outp.write('Function %s uses a for-loop, which is not allowed.\n' % repr(func))
        score = 0
        if not step:
            return (FAIL_INCORRECT,max(0,score))
    elif found3:
        outp.write('Function %s uses recursion, which is not allowed.\n' % repr(func))
        score -= 0.5
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
    crashes = status
    
    func = 'put_in'
    if not crashes:
        outp.write("Comments for %s:\n" % repr(func))
        status, p2a = grade_func1(file,1,outp)
        if not status:
           status, p2b = grade_structure(file,func,1,outp)
        else:
            p2b = 0
        p2 = 0.8*p2a+0.2*p2b
        if p2 == 1:
            outp.write('The function looks good.\n\n')
        else:
            outp.write('\n')
    else:
        p2 = 0
    
    func = 'rotate'
    if not crashes:
        outp.write("Comments for %s:\n" % repr(func))
        status, p3a = grade_func2(file,1,outp)
        if not status:
           status, p3b = grade_structure(file,func,1,outp)
        else:
            p3b = 0
        p3 = 0.8*p3a+0.2*p3b
        if p3 == 1:
            outp.write('The function looks good.\n\n')
        else:
            outp.write('\n')
    else:
        p3 = 0
    
    total = round(0.05*p1+0.45*p2+0.5*p3,3)
    return total


def grade(outp=sys.stdout):
    """
    Invokes this subgrader (returning a percentage)
    """
    return grade_file('funcs.py',outp)


if __name__ == '__main__':
    print(grade())