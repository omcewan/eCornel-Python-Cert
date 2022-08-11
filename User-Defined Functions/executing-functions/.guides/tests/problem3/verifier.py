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
from modlib import Environment

# #mark Constants

# The status codes
TEST_SUCCESS      = 0
FAIL_NO_FILE      = 1
FAIL_BAD_STYLE    = 2
FAIL_CRASHES      = 4
FAIL_INCORRECT    = 5


WORKSPACE = [os.path.expanduser('~'),'workspace','exercise3']
#WORKSPACE = []


# #mark -
# #mark Helpers
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


def import_module(name,first=1,last=6):
    """
    Returns a reference to the module.
    
    Returns an error message if it fails.
    
    Parameter name: The module name
    Precondition: name is a string
    """
    try:
        refs = os.path.splitext(name)[0]
        environment = Environment(refs,WORKSPACE,first,last)
        environment.execute()
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


pass
# #mark -
# #mark Verification
def grade_global(file,step=0,outp=sys.stdout):
    """
    Returns the test result and score for the global variable increment.
    
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
    score = 1
    env = import_module(file)
    if type(env) == str:
        outp.write(env)
        return (FAIL_CRASHES,0)
    elif not hasattr(env.module,'next'):
        outp.write("File %s is missing the header for 'next'.\n" % repr(file))
        return (FAIL_INCORRECT,0)
    elif not hasattr(env.module,'VAR'):
        outp.write("File %s is missing the global variable 'VAR'.\n" % repr(file))
        return (FAIL_INCORRECT,0)
    
    if env.module.next.__code__.co_argcount != 0:
        outp.write("Function next does not have the right number of arguments.\n")
        return (FAIL_INCORRECT,0)
    
    args = env.module.next.__code__.co_varnames
    if 'VAR' in args:
        outp.write("Function next does not use the global keyword.\n")
        score -= 0.4
        if not step:
            return (FAIL_INCORRECT, max(0,score))
    
    if len(env.printed) != 0:
        outp.write('File %s has print statements.\n' % repr(file))
        score -= 0.1
        if not step:
            return (FAIL_INCORRECT, max(0,score))
    
    old = env.module.VAR
    try:
        result = env.module.next()
    except:
        result = None
        outp.write("File %s has a major syntax error.\n" % repr(file))
        outp.write(traceback.format_exc(0))
        return (FAIL_CRASHES,0)
    
    if len(env.printed) != 0:
        outp.write('Function next has print statements.\n')
        score -= 0.2
        if not step:
            return (FAIL_INCORRECT, max(0,score))
    
    if env.module.VAR != old+1:
        outp.write("Function next does not increment 'VAR' correctly.\n")
        score -= 0.4
        if not step:
            return (FAIL_INCORRECT, max(0,score))
    
    try:
        result = env.module.next()
    except:
        result = None
        outp.write("File %s has a major syntax error.\n" % repr(file))
        outp.write(traceback.format_exc(0))
        return (FAIL_CRASHES, 0)
    
    if env.module.VAR != old+2:
        outp.write("Function next does not increment 'VAR' correctly [2nd Attempt].\n")
        score -= 0.4
        if not step:
            return (FAIL_INCORRECT, max(0,score))
    
    return (TEST_SUCCESS,max(0,score))


def grade_body(file,step=0,outp=sys.stdout):
    """
    Returns the test result for the function body.
    
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
    score = 1
    env = import_module(file)
    if type(env) == str:
        outp.write(env)
        return (FAIL_CRASHES,0)
    elif not hasattr(env.module,'next'):
        outp.write("File %s is missing the header for 'next'.\n" % repr(file))
        return (FAIL_INCORRECT,0)
    elif not hasattr(env.module,'VAR'):
        outp.write("File %s is missing the global variable 'VAR'.\n" % repr(file))
        return (FAIL_INCORRECT,0)
    
    old = env.module.VAR
    try:
        result = env.module.next()
    except:
        result = None
        outp.write("File %s has a major syntax error.\n" % repr(file))
        outp.write(traceback.format_exc(0))
        return (FAIL_CRASHES,0)
    
    if len(env.printed) != 0:
        outp.write('Function next has print statements.\n')
        score -= 0.2
        if not step:
            return (FAIL_INCORRECT,max(0,score))
    if result is None:
        outp.write("Function next is missing a return statement.\n")
        return (FAIL_INCORRECT,0)
    elif result != old:
        outp.write("Function next does not return the correct value.\n")
        score -= 0.4
        if not step:
            return (FAIL_INCORRECT,max(0,score))
    
    try:
        result = env.module.next()
    except:
        result = None
        outp.write("File %s has a major syntax error.\n" % repr(file))
        outp.write(traceback.format_exc(0))
        return (FAIL_CRASHES,0)
    if result is None:
        outp.write('Function next uses if-statements.\n')
        return (FAIL_INCORRECT,max(score-0.5,0))
    elif result != old+1:
        outp.write("Function next does not return the correct value.\n")
        score -= 0.4
        if not step:
            return (FAIL_INCORRECT,max(0,score))
    
    return (TEST_SUCCESS, max(0,score))


# #mark -
# #mark Main Graders
def grade_file(file,outp=sys.stdout):
    """
    Grades the interactive script, weighting earlier parts less.
    
    Parameter name: The file name
    Precondition: name is a string
    
    Parameter outp: The output stream
    Precondition: outp is a stream writer
    """
    outp.write('Global variable comments:\n')
    status, p1 = grade_global(file,1,outp)
    if p1 == 1:
        outp.write('The global variable behaves correctly.\n\n')
    else:
        outp.write('\n')
    
    if not status:
        outp.write('Body comments:\n')
        status, p2 = grade_body(file,1,outp)
        if p2 == 1:
            outp.write('The function body looks good.\n\n')
        else:
            outp.write('\n')
    else:
        p2 = 0
    
    total = round(0.5*p1+0.5*p2,3)
    return total


def grade(outp=sys.stdout):
    """
    Invokes this subgrader (returning a percentage)
    """
    return grade_file('glob.py',outp)


if __name__ == '__main__':
    print(grade())
