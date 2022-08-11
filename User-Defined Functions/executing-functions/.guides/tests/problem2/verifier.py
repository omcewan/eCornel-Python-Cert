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


WORKSPACE = [os.path.expanduser('~'),'workspace','exercise2']
#WORKSPACE = []


DOCSTRING =  """
    Returns the sum of two random numbers.
    
    The numbers generated are between first and last (inclusive).  
    
    Example: rollem(1,6) can return any value between 2 and 12.
    
    Parameter first: The lowest possible number
    Precondition: first is an integer
    
    Parameter last: The greatest possible number
    Precondition: last is an integer, last >= first
    """


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


# Localized error codes
PRINT_FIRST_NO_PERIOD = 1
PRINT_FIRST_NO_MATCH  = 2
PRINT_SECND_NO_PERIOD = 3
PRINT_SECND_NO_MATCH  = 4

def check_print(env,first,last,correct):
    """
    Returns TEST_SUCCESS if the output is correct, and error code otherwise
    
    Parameter env: The execution environment.
    Precondition: env is a instance of environment
    
    Parameter first: The lowest random number
    Precondition: first is an integer
    
    Parameter last: The greatest random number
    Precondition: last is an integer
    
    Parameter correct: The correct answer
    Precondition: correct is an integer (or None)
    """
    display1 = 'Choosing two numbers between '+str(first)+' and '+str(last)+'.'
    display2 = 'The sum is '+str(correct)+'.'
    actual1 = env.printed[0].strip()
    if actual1 == display1[:-1]:
        return PRINT_FIRST_NO_PERIOD
    elif actual1 != display1:
        return PRINT_FIRST_NO_MATCH
    
    if not correct is None:
        actual2 = env.printed[1].strip()
        if actual2 == display2[:-1]:
            return PRINT_SECND_NO_PERIOD
        elif actual2 != display2:
            return PRINT_SECND_NO_MATCH
    
    return TEST_SUCCESS

pass
# #mark -
# #mark Verification
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
            outp.write("The second-to-last line does not start with 'Author:'\n")
            score -= 0.3
        if test == NAME_INCOMPLETE:
            outp.write("There is no name after 'Author:'\n")
            score -= 0.1
        if not step:
            return (FAIL_BAD_STYLE,max(0,score))
    test = check_date(docs)
    if test:
        if test == DATE_MISSING:
            outp.write("The last line does not start with 'Date:'\n")
            score -= 0.2
        if test == DATE_INCOMPLETE:
            outp.write("The date after 'Date:' is invalid.\n")
            score -= 0.1
        if not step:
            return (FAIL_BAD_STYLE, max(0,score))
    
    return (TEST_SUCCESS, max(0,score))


def grade_procedure(file,step=0,outp=sys.stdout):
    """
    Returns the test result and score  for the procedure version of rollem
    
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
    code = read_file(file)
    if code is None:
        outp.write('Could not find the file %s.\n' % repr(file))
        return (FAIL_NO_FILE,0)
    
    env = import_module(file)
    if type(env) == str:
        outp.write(env)
        return (FAIL_CRASHES, 0)
    elif not hasattr(env.module,'rollem'):
        outp.write("File %s is missing the header for rollem.\n" % repr(file))
        return (FAIL_INCORRECT, 0)
    
    if env.module.rollem.__code__.co_argcount != 2:
        outp.write("Procedure rollem does not have the right number of arguments.\n")
        return (FAIL_INCORRECT, max(score-0.7,0))
    
    args = env.module.rollem.__code__.co_varnames
    if args[0] != 'first':
        outp.write("Procedure rollem does not have 'first' as its first parameter.\n")
        score -= 0.1
        if not step:
            return (FAIL_INCORRECT, max(0,score))
    if args[1] != 'last':
        outp.write("Procedure rollem does not have 'last' as its second parameter.\n")
        score -= 0.1
        if not step:
            return (FAIL_INCORRECT, max(0,score))
    
    count = 2
    import random
    random.seed(10)
    
    FIRST = 1
    LAST  = 6
    try:
        result = env.module.rollem(FIRST,LAST)
    except:
        result = None
        outp.write("File %s has a major syntax error.\n" % repr(file))
        outp.write(traceback.format_exc(0))
        return (FAIL_CRASHES,0)
    
    if len(env.printed) != count:
        outp.write('Procedure rollem has the wrong number of print statements (expected %d).\n' % count)
        score -= 0.15
        if not step:
            return (FAIL_INCORRECT, max(0,score))
    elif (not result is None):
        outp.write('Procedure rollem has a return statement.\n')
        score -= 0.1
        if not step:
            return (FAIL_INCORRECT, max(0,score))
    
    err = check_print(env,FIRST,LAST,6)
    if err:
        if err == PRINT_FIRST_NO_PERIOD:
            outp.write('The first print statement is missing a period.\n')
            score -= 0.05
            err = FAIL_BAD_STYLE
        elif err == PRINT_FIRST_NO_MATCH:
            outp.write('The first print statement is incorrect.\n')
            score -= 1
            err = FAIL_INCORRECT
        if err == PRINT_SECND_NO_PERIOD:
            outp.write('The second print statement is missing a period.\n')
            score -= 0.05
            err = FAIL_BAD_STYLE
        elif err == PRINT_SECND_NO_MATCH:
            outp.write('The second print statement is incorrect.\n')
            score -= 2
            err = FAIL_INCORRECT
        if not step:
            return (err,max(0,score))
    
    FIRST = -3
    LAST  = 5
    env.reset()
    
    try:
        result = env.module.rollem(FIRST,LAST)
    except:
        result = None
        outp.write("File %s has a major syntax error.\n" % repr(file))
        outp.write(traceback.format_exc(0))
        return (FAIL_CRASHES,0)
    
    if len(env.printed) != count:
        outp.write('Procedure rollem has the wrong number of print statements (expected %d) [2nd Attempt].\n' % count)
        score -= 0.15
        if not step:
            return (FAIL_INCORRECT, max(0,score))
    elif (not result is None):
        outp.write('Procedure rollem has a return statement [2nd Attempt].\n')
        score -= 0.1
        if not step:
            return (FAIL_INCORRECT, max(0,score))
    
    err = check_print(env,FIRST,LAST,7)
    if err:
        if err == PRINT_FIRST_NO_PERIOD:
            outp.write('The first print statement is missing a period [2nd Attempt].\n')
            score -= 0.05
            err = FAIL_BAD_STYLE
        elif err == PRINT_FIRST_NO_MATCH:
            outp.write('The first print statement is incorrect [2nd Attempt].\n')
            score -= 1
            err = FAIL_INCORRECT
        if err == PRINT_SECND_NO_PERIOD:
            outp.write('The second print statement is missing a period [2nd Attempt].\n')
            score -= 0.05
            err = FAIL_BAD_STYLE
        elif err == PRINT_SECND_NO_MATCH:
            outp.write('The second print statement is incorrect [2nd Attempt].\n')
            score -= 2
            err = FAIL_INCORRECT
        if not step:
            return (err,max(0,score))
    
    if not 'random.randint' in code:
        outp.write('The function does not create random numbers.\n')
        score -= 0.5
        if not step:
            return (FAIL_INCORRECT,max(0,score))
        
    vars = env.module.rollem.__code__.co_varnames
    if not 'thesum' in vars:
        outp.write('Procedure rollem is missing the variable %s' % repr('thesum'))
        score -= 0.35
        if not step:
            return (FAIL_INCORRECT,max(0,score))
    
    return (TEST_SUCCESS,max(0,score))


def grade_body(file,step=0,outp=sys.stdout):
    """
    Returns the test result and score  for whether the prints were removed correctly.
    
    The step parameter is the phase in the grading pass.  Step 0 only looks at the 
    calculation and ignores the return value.  Step 1 looks for a return value.
    Steps 0 and 1 will stop at the first error found.  Step 2 is the final grading 
    pass and will continue through and try to find all errors.
    
    Parameter name: The file name
    Precondition: name is a string of a file in the given workspace
    
    Parameter step: The current verfication/grading step
    Precondition: grade is 0, 1, or 2
    
    Parameter outp: The output stream
    Precondition: outp is a stream writer
    """
    score = 1
    code = read_file(file)
    if code is None:
        outp.write('Could not find the file %s.\n' % repr(file))
        return (FAIL_NO_FILE,0)
    
    env = import_module(file)
    if type(env) == str:
        outp.write(env)
        return (FAIL_CRASHES,0)
    elif not hasattr(env.module,'rollem'):
        outp.write("File %s is missing the header for rollem.\n" % repr(file))
        return (FAIL_INCORRECT,0)
    elif len(env.printed) > 0:
        outp.write('File %s has print statement outside of the function body.\n' % repr(file))
        score -= 0.15
        if step < 2:
            return (FAIL_INCORRECT, max(0,score))
    
    if not 'random.randint' in code:
        outp.write('You removed the lines creating random numbers.\n')
        return (FAIL_INCORRECT,0)
    if step > 0 and not 'return ' in code:
        outp.write('The function rollem is missing a return statement.\n')
        return (FAIL_INCORRECT,max(score-0.9,0))
    
    if env.module.rollem.__code__.co_argcount != 2:
        outp.write("Function rollem does not have the right number of arguments.\n")
        return (FAIL_INCORRECT,0)
    args = env.module.rollem.__code__.co_varnames
    if args[0] != 'first':
        outp.write("Function rollem does not have 'first' as its first parameter.\n")
        score -= 0.1
        if step < 2:
            return (FAIL_INCORRECT,max(0,score))
    if args[1] != 'last':
        outp.write("Function rollem does not have 'last' as its second parameter.\n")
        score -= 0.1
        if step < 2:
            return (FAIL_INCORRECT,max(0,score))
    vars = env.module.rollem.__code__.co_varnames
    if not 'thesum' in vars:
        outp.write('You removed the variable %s from the function rollem.\n' % repr('thesum'))
        score -= 0.1
        if step < 2:
            return (FAIL_INCORRECT,max(0,score))
    
    import random
    random.seed(10)
    
    FIRST = 1
    LAST  = 6
    
    try:
        result = env.module.rollem(FIRST,LAST)
    except:
        result = None
        outp.write("File %s has a major syntax error.\n" % repr(file))
        outp.write(traceback.format_exc(0))
        return (FAIL_CRASHES,0)
    
    if len(env.printed) != 0:
        outp.write('The function rollem still has print statements.\n')
        score -= 0.15
        if step < 2:
            return (FAIL_INCORRECT,max(0,score))
    if step > 0 and result is None:
        outp.write('Function rollem is missing a return statement.\n')
        return (FAIL_INCORRECT,max(score-0.9,0))
    if step > 0 and result != 6:
        outp.write('Function rollem returns the wrong value.\n')
        score -= 0.3
        if step < 2:
            return (FAIL_INCORRECT,max(0,score))
    
    if step > 0:
        FIRST = -3
        LAST  = 5
        env.reset()
    
        try:
            result = env.module.rollem(FIRST,LAST)
        except:
            result = None
            outp.write("File %s has a major syntax error.\n" % repr(file))
            outp.write(traceback.format_exc(0))
            return (FAIL_CRASHES,0)
        
        if result is None:
            outp.write('Function rollem uses if-statements.\n')
            return (FAIL_INCORRECT,max(score-0.5,0))
        if result != 7:
            outp.write('Function rollem returns the wrong value [2nd Attempt].\n')
            score -= 0.3
            if step < 2:
                return (FAIL_INCORRECT,max(0,score))
    
    return (TEST_SUCCESS, max(0,score))


def grade_spec(file,step=0,outp=sys.stdout):
    """
    Returns the test result and score for the function specification
    
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
        return (FAIL_CRASHES, 0)
    elif not hasattr(env.module,'rollem'):
        outp.write("File %s is missing the header for rollem.\n" % repr(file))
        return (FAIL_INCORRECT, 0)
    elif not env.module.rollem.__doc__:
        outp.write("Function rollem does not have a docstring.\n")
        return (FAIL_INCORRECT, 0)
    
    correct = [ x.strip().lower() for x in DOCSTRING.split()]
    correct = list(filter(lambda x : len(x) > 0, correct))
    actuals = [ x.strip().lower() for x in env.module.rollem.__doc__.split()]
    actuals = list(filter(lambda x : len(x) > 0, actuals))
    if (correct != actuals):
        outp.write("Function rollem does not have the correct docstring.\n")
        score -= 0.8
        return (FAIL_INCORRECT, max(0,score))
    
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
    outp.write('Module docstring comments:\n')
    status, p1 = grade_docstring(file,1,outp)
    if p1 == 1:
        outp.write('The docstring looks good.\n\n')
    else:
        outp.write('\n')
    
    if not status:
        outp.write('Body comments:\n')
        status, p2 = grade_body(file,2,outp)
        if p2 == 1:
            outp.write('The function body looks good.\n\n')
        else:
            outp.write('\n')
    else:
        p2 = 0
    
    if not status:
        outp.write('Function docstring comments:\n')
        status, p3 = grade_spec(file,1,outp)
        if p3 == 1:
            outp.write('The function docstring looks good.\n\n')
        else:
            outp.write('\n')
    else:
        p3 = 0
    
    total = round(0.2*p1+0.7*p2+0.1*p3,3)
    return total


def grade(outp=sys.stdout):
    """
    Invokes this subgrader (returning a percentage)
    """
    return grade_file('func.py',outp)


if __name__ == '__main__':
    print(grade())
