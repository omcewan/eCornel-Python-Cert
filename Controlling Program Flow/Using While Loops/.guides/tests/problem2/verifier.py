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
import ast
from modlib import WhileEnvironment

# For support
import introcs

#mark Constants

# The status codes
TEST_SUCCESS      = 0
FAIL_NO_FILE      = 1
FAIL_BAD_STYLE    = 2
FAIL_CRASHES      = 4
FAIL_INCORRECT    = 5


WORKSPACE = [os.path.expanduser('~'),'workspace','exercise2']
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


def import_module(name):
    """
    Returns a reference to the module.
    
    Returns an error message if it fails.
    
    Parameter name: The module name
    Precondition: name is a string
    """
    try:
        import types
        refs = os.path.splitext(name)[0]
        environment = WhileEnvironment(refs,WORKSPACE)
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


def verify_trace1(file,step=0,outp=sys.stdout):
    """
    Verifies that a limiter and a trace statement was properly added to flips
    
    The parameter step separates the limiter from the trace. If step is 0, it just
    looks for the limiter. If step is 1, it looks for the trace as well.
    
    Parameter file: The file name
    Precondition: file is a string of a file in the given workspace
    
    Parameter step: The current verfication step
    Precondition: step is 0 or 1
    
    Parameter outp: The output stream
    Precondition: outp is a stream writer
    """
    WhileEnvironment.LIMIT = 20
    debugLimit = 10

    env = import_module(file)
    
    function = 'flips'
    import random
    random.seed(20)
    
    if type(env) == str:
        outp.write(env)
        return (FAIL_CRASHES, 0)
    elif not hasattr(env.module,function):
        outp.write("File %s is missing the header for %s.\n" % (repr(file),repr(function)))
        return (FAIL_INCORRECT, 0)
    elif not hasattr(env.module,'__whileguard__'):
        outp.write("File %s was not properly processed by the autograder.\n" % repr(file))
        return (FAIL_INCORRECT, 0)
    
    func = getattr(env.module,function)
    try:
        env.reset()
        received = func()
        if len(env.printed) > 0:
            same = True
            for item in env.printed:
                same = same and item == env.printed[0]
        else:
            same = False
        
        if env.module.__whileguard__ == env.LIMIT:
            outp.write('You have not properly added the limiting code to %s.\n' % repr(function))
            return (FAIL_INCORRECT, 0)
        elif env.module.__whileguard__ > debugLimit+1:
            outp.write('You have not limited the while-loop in %s to %d tries.\n' % (repr(function),debugLimit))
            return (FAIL_INCORRECT, 0)
        elif step == 0 and env.module.__whileguard__ < debugLimit+1:
            outp.write('It appears you tried to fix the bug in %s, before being asked to.\n' % repr(function))
            return (FAIL_INCORRECT, 0)
        elif step:
            if len(env.printed) < env.module.__whileguard__:
                outp.write("You are not printing out 'going' every loop iteration.\n")
                return (FAIL_INCORRECT, 0)
            elif len(env.printed) > debugLimit+1 and same:
                outp.write("You put the print statement in the wrong place.\n")
                return (FAIL_INCORRECT, 0)
            elif len(env.printed) > debugLimit+1:
                outp.write("You have added extra debugging statements.  Only print out 'going' at this step.\n")
                return (FAIL_INCORRECT, 0)
            else:
                miss = False
                for line in env.printed:
                    if not 'True' in line:
                        miss = True
            
                if miss:
                    outp.write("The debug statement in %s does not always print the value of 'going'.\n" % repr(function))
                    return (FAIL_INCORRECT, 0)
    except:
        import traceback
        outp.write("The call %s() crashed.\n" % function)
        outp.write(traceback.format_exc(0)+'\n')
        return (FAIL_INCORRECT, 0)
    
    return (TEST_SUCCESS,1)


def grade_func1(file,step=0,outp=sys.stdout):
    """
    Returns the test result and score for the implementation of flips
    
    The step parameter is the phase in the grading pass.  Step 0 is a verification step
    and will stop at the first error found.  Step 1 makes sure all print statements 
    are removed. Steps 0 and 1 are verification steps and will stop at the first error 
    found.Otherwise it will continue through and try to find all errors.
    
    Parameter file: The file name
    Precondition: file is a string of a file in the given workspace
    
    Parameter step: The current verfication/grading step
    Precondition: grade is 0 or 1
    
    Parameter outp: The output stream
    Precondition: outp is a stream writer
    """
    WhileEnvironment.LIMIT = 999
    score = 1
    env = import_module(file)
    
    function = 'flips'
    
    import random
    random.seed(20)
    outputs = [1,1,2,0,3,0,0,0,2,0,0,0,1,0,8,0,0,0,3]
    
    if type(env) == str:
        outp.write(env)
        return (FAIL_CRASHES, 0)
    elif not hasattr(env.module,function):
        outp.write("File %s is missing the header for %s.\n" % (repr(file),repr(function)))
        return (FAIL_INCORRECT, 0)
    elif not hasattr(env.module,'__whileguard__'):
        outp.write("File %s was not properly processed by the autograder.\n" % repr(file))
        return (FAIL_INCORRECT, 0)
    
    func = getattr(env.module,function)
    for expected in outputs:
        try:
            env.reset()
            received = func()
            if env.module.__whileguard__ >= env.LIMIT:
                outp.write("The function %s has an infinite loop in it.\n" % repr(function))
                outp.write("Stopped loop after %d iterations.\n" % env.module.__whileguard__)
                score -= 1/len(outputs)
                if step < 2:
                    return (FAIL_INCORRECT,max(0,score))
            elif received != expected:
                outp.write("The function %s returned %d when %d was expected.\n" % (repr(function), received, expected))
                score -= 1/len(outputs)
                if step < 2:
                    return (FAIL_INCORRECT,max(0,score))
        except:
            import traceback
            outp.write("The call %s() crashed.\n" % function)
            outp.write(traceback.format_exc(0)+'\n')
            score -= 1/len(testcase)
            if step < 2:
                return (FAIL_INCORRECT,max(0,score))
    
    if step > 0 and len(env.printed) != 0:
        outp.write("You must remove all debugging print statements from %s.\n" % repr(function))
        score -= 0.1
        if step < 2:
            return (FAIL_BAD_STYLE,max(0,score))
    
    return (TEST_SUCCESS,max(0,score))


def verify_trace2(file,step,outp=sys.stdout):
    """
    Verifies that a trace statement was properly added to partition
    
    The parameter step separates the limiter from the trace. If step is 0, it just
    looks for the limiter. If step is 1, it looks for the trace as well.
    
    Parameter file: The file name
    Precondition: file is a string of a file in the given workspace
    
    Parameter step: The current verfication step
    Precondition: step is 0 or 1
    Parameter outp: The output stream
    Precondition: outp is a stream writer
    """
    WhileEnvironment.LIMIT = 20
    debugLimit = 10
    
    env = import_module(file)
    
    function = 'partition'
    input  = 'school'
    output = [0,1,2,3,3,3,3,3,3,3,3]
    
    if type(env) == str:
        outp.write(env)
        return (FAIL_CRASHES, 0)
    elif not hasattr(env.module,function):
        outp.write("File %s is missing the header for %s.\n" % (repr(file),repr(function)))
        return (FAIL_INCORRECT, 0)
    elif not hasattr(env.module,'__whileguard__'):
        outp.write("File %s was not properly processed by the autograder.\n" % repr(file))
        return (FAIL_INCORRECT, 0)
    
    func = getattr(env.module,function)
    try:
        received = func(input)
        if env.module.__whileguard__ == env.LIMIT:
            outp.write('You have not properly added the limiting code to %s.\n' % repr(function))
            return (FAIL_INCORRECT, 0)
        elif env.module.__whileguard__ > debugLimit+1:
            outp.write('You have not limited the while-loop in %s to %d tries.\n' % (repr(function),debugLimit))
            return (FAIL_INCORRECT, 0)
        elif step == 0 and env.module.__whileguard__ < debugLimit+1:
            outp.write('It appears you tried to fix the bug in %s, before being asked to.\n' % repr(function))
            return (FAIL_INCORRECT, 0)
        elif step:
            #Changing below condition from '< env.module.__whileguard__' to '< debugLimit' - 10/30/2022 -TB
            if len(env.printed) < debugLimit:
                outp.write("You are not printing out 'pos' every loop iteration.\n")
                return (FAIL_INCORRECT, 0)
            elif len(env.printed) > debugLimit:
                #Appending additional error message to below from 'and' - 10/30/2022 -TB
                outp.write("You have added extra debugging statements.  Only print out 'pos' at this step, and ensure the print(pos) statement is on the correct line.\n")
                return (FAIL_INCORRECT, 0)
            else:
                miss = False
                for pos in range(len(env.printed)):
                    line = env.printed[pos]
                    x = pos+1
                    try:
                        x = int(line)
                    except:
                        pass
                    if not str(output[pos]) in line and x != pos:
                        miss = True
            
                if miss:
                    outp.write("The debug statement in %s does not always print the value of 'pos'.\n" % repr(function))
                    return (FAIL_INCORRECT, 0)
    except:
        import traceback
        outp.write("The call %s(%s) crashed.\n" % (function,repr(input)))
        outp.write(traceback.format_exc(0)+'\n')
        return (FAIL_INCORRECT, 0)
    
    return (TEST_SUCCESS,1)


def grade_func2(file,step=0,outp=sys.stdout):
    """
    Returns the test result and score for the implementation of partition
    
    The step parameter is the phase in the grading pass.  Step 0 is a verification step
    and will stop at the first error found.  Step 1 makes sure all print statements 
    are removed. Steps 0 and 1 are verification steps and will stop at the first error 
    found.Otherwise it will continue through and try to find all errors.
    
    Parameter file: The file name
    Precondition: file is a string of a file in the given workspace
    
    Parameter step: The current verfication/grading step
    Precondition: grade is 0 or 1
    
    Parameter outp: The output stream
    Precondition: outp is a stream writer
    """
    WhileEnvironment.LIMIT = 999
    score = 1
    env = import_module(file)
    
    function = 'partition'
    testcase = [('y',('','y')),('hello',('eo','hll')),('superstar',('uea','sprstr')),
                ('grxlpk',('','grxlpk')),('aeiou',('aeiou','')),('generous',('eeou','gnrs')),
                ('scary',('a','scry'))]
    
    if type(env) == str:
        outp.write(env)
        return (FAIL_CRASHES, 0)
    elif not hasattr(env.module,function):
        outp.write("File %s is missing the header for %s.\n" % (repr(file),repr(function)))
        return (FAIL_INCORRECT, 0)
    elif not hasattr(env.module,'__whileguard__'):
        outp.write("File %s was not properly processed by the autograder.\n" % repr(file))
        return (FAIL_INCORRECT, 0)
    
    func = getattr(env.module,function)
    for pair in testcase:
        try:
            expected = pair[1]
            received = func(pair[0])
            if env.module.__whileguard__ >= env.LIMIT:
                outp.write("The call %s(%s) encountered an infinite loop.\n" % (function,repr(pair[0])))
                outp.write("Stopped loop after %d iterations.\n" % env.module.__whileguard__)
                score -= 1/len(testcase)
                if not step:
                    return (FAIL_INCORRECT,max(0,score))
            elif received != expected:
                outp.write("The call %s(%s) returns %s, not %s.\n" % (function, repr(pair[0]), repr(received), repr(expected)))
                score -= 1/len(testcase)
                if not step:
                    return (FAIL_INCORRECT,max(0,score))
        except:
            import traceback
            outp.write("The call %s(%s) crashed.\n" % (function,repr(pair[0])))
            outp.write(traceback.format_exc(0)+'\n')
            score -= 1/len(testcase)
            if not step:
                return (FAIL_INCORRECT,max(0,score))
    
    if step > 0 and len(env.printed) != 0:
        outp.write("You must remove all debugging print statements from %s.\n" % repr(function))
        score -= 0.1
        if step < 2:
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
    found4 = False
    for item in ast.walk(body):
        if type(item) == ast.While:
            found1 = True
        elif type(item) == ast.For:
            found2 = True
        elif type(item) == ast.Call and type(item.func) == ast.Name and item.func.id == func:
            found3 = True
        elif type(item) == ast.Break:
            found4 = True
        
    
    if found2:
        outp.write('Function %s uses a for-loop, which is not allowed.\n' % repr(func))
        score -= 0.5
        if not step:
            return (FAIL_INCORRECT,max(0,score))
    elif not found1:
        outp.write('Function %s does not have a while-loop in it.\n' % repr(func))
        score = 0
        if not step:
            return (FAIL_INCORRECT,max(0,score))
    
    if found3:
        outp.write('Function %s uses recursion, which is not allowed.\n' % repr(func))
        score -= 0.5
        if not step:
            return (FAIL_INCORRECT,max(0,score))
    
    if found4:
        outp.write('Function %s still has the limiting code, which should be removed.\n' % repr(func))
        score -= 0.25
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
    func = 'flips'
    outp.write("Comments for %s:\n" % repr(func))
    status, p1a = grade_func1(file,2,outp)
    if not status:
       status, p1b = grade_structure(file,func,1,outp)
    else:
        p1b = 0
    p1 = 0.8*p1a+0.2*p1b
    if p1 == 1:
        outp.write('The function looks good.\n\n')
    else:
        outp.write('\n')
    
    func = 'partition'
    outp.write("Comments for %s:\n" % repr(func))
    status, p2a = grade_func2(file,2,outp)
    if not status:
       status, p2b = grade_structure(file,func,1,outp)
    else:
        p2b = 0
    p2 = 0.8*p2a+0.2*p2b
    if p2 == 1:
        outp.write('The function looks good.\n\n')
    else:
        outp.write('\n')
    
    total = round(0.5*p1+0.5*p2,3)
    return total


def grade(outp=sys.stdout):
    """
    Invokes this subgrader (returning a percentage)
    """
    return grade_file('funcs.py',outp)


if __name__ == '__main__':
    print(grade())