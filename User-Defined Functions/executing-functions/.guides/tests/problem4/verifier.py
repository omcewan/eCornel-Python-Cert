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
FAIL_BAD_VALUE    = 3
FAIL_CRASHES      = 4
FAIL_INCORRECT    = 5


WORKSPACE = [os.path.expanduser('~'),'workspace','exercise4']
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
PRINT_WRONG_LINES = 1
PRINT_NO_PERIOD   = 2
PRINT_FIRST_MATCH = 3
PRINT_SECND_MATCH = 4

def check_print(env,p1,p2):
    """
    Returns TEST_SUCCESS if the output is correct, and error code otherwise
    
    Parameter env: The execution environment.
    Precondition: env is a instance of environment
    
    Parameter p1: The result for player 1
    Precondition: p1 is an integer
    
    Parameter p2: The result for player 2
    Precondition: p2 is an integer
    """
    if len(env.printed) != 1:
        return PRINT_WRONG_LINES
    
    display ='Player 1 got '+str(p1)+'; Player 2 got '+str(p2)+'.'
    actuals = env.printed[0].strip()
    if actuals == display[:-1]:
        return PRINT_NO_PERIOD
    elif actuals != display:
        left = actuals[:actuals.find(';')]
        rght = display[:display.find(';')]
        if left == rght:
            return PRINT_SECND_MATCH
        return PRINT_FIRST_MATCH
    
    return TEST_SUCCESS


pass
# #mark -
# #mark Verification
def grade_helper(file,step=0,outp=sys.stdout):
    """
    Returns the test result and score for whether the helper rollem is correct.
    
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
    elif not hasattr(env.module,'rollem'):
        outp.write("File %s is missing the header for rollem.\n" % repr(file))
        return (FAIL_NO_VALUE,0)
    
    code = env.module.rollem.__code__
    if not 'random' in code.co_names or not 'randint' in code.co_names:
        outp.write('You removed the lines creating random numbers.\n')
        return (FAIL_INCORRECT,0)
    
    if env.module.rollem.__code__.co_argcount != 2:
        outp.write("Function rollem does not have the right number of arguments.\n")
        return (FAIL_BAD_VALUE,0)
    args = env.module.rollem.__code__.co_varnames
    if args[0] != 'first':
        outp.write("Function rollem does not have 'first' as its first parameter.\n")
        score -= 0.1
        if not step:
            return (FAIL_INCORRECT, max(0,score))
    if args[1] != 'last':
        outp.write("Function rollem does not have 'last' as its second parameter.\n")
        score -= 0.1
        if not step:
            return (FAIL_INCORRECT, max(0,score))
    vars = env.module.rollem.__code__.co_varnames
    if not 'thesum' in vars:
        outp.write('You removed the variable %s from the function rollem.\n' % repr('thesum'))
        score -= 0.1
        if not step:
            return (FAIL_INCORRECT, max(0,score))
    
    import random
    random.seed(10)
    
    FIRST = 1
    LAST  = 6
    
    try:
        result = env.module.rollem(FIRST,LAST)
    except:
        result = None
        outp.write("Function rollem has a major syntax error.\n")
        outp.write(traceback.format_exc(0))
        return (FAIL_CRASHES,0)
    
    if len(env.printed) != 0:
        outp.write('The function rollem still has print statements.\n')
        score -= 0.2
        if not step:
            return (FAIL_INCORRECT, max(0,score))
    if result is None:
        outp.write('Function rollem is missing a return statement.\n')
        score -= 0.5
        if not step:
            return (FAIL_INCORRECT, max(0,score))
    if result != 6:
        outp.write('Function rollem returns the wrong value.\n')
        score -= 0.3
        if not step:
            return (FAIL_INCORRECT, max(0,score))
    
    FIRST = -3
    LAST  = 5
    env.reset()
    
    try:
        result = env.module.rollem(FIRST,LAST)
    except:
        result = None
        outp.write("Function rollem has a major syntax error.\n")
        outp.write(traceback.format_exc(0))
        return (FAIL_CRASHES,0)
    
    if result is None:
        outp.write('Function rollem uses if-statements.\n')
        return (FAIL_INCORRECT, max(0,score-0.5))
    if result != 7:
        outp.write('Function rollem returns the wrong value [2nd Attempt].\n')
        score -= 0.3
        if not step:
            return (FAIL_INCORRECT, max(0,score))
    
    return (TEST_SUCCESS, max(0,score))


def grade_player1(file,step=0,outp=sys.stdout):
    """
    Returns the test result and score for the first player
    
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
    elif not hasattr(env.module,'roll_off'):
        outp.write("File %s is missing the header for roll_off.\n" % repr(file))
        return (FAIL_INCORRECT,0)
    
    code = env.module.roll_off.__code__
    if not 'rollem' in code.co_names:
        outp.write("Function roll_off does not call rollem as a helper.\n")
        score -= 0.5
        if not step:
            return (FAIL_INCORRECT, max(0,score))
    
    import random
    random.seed(10)
    
    PLAYER1 = 0
    PLAYER2 = 0
    
    try:
        result = env.module.roll_off(PLAYER1,PLAYER2)
    except:
        result = None
        outp.write("Function roll_off has a major syntax error.\n")
        outp.write(traceback.format_exc(0))
        return (FAIL_CRASHES,0)
    
    error = check_print(env,6,8)
    if error == PRINT_WRONG_LINES:
        outp.write("Function roll_off has the wrong number of print statements: either more than one, or none.\n")
        score -= 0.2
        if not step:
            return (FAIL_INCORRECT, max(0,score))
    elif error == PRINT_NO_PERIOD:
        outp.write("The print statement in roll_off is missing a period.\n")
        score -= 0.05
        if not step:
            return (FAIL_INCORRECT, max(0,score))
    elif error == PRINT_FIRST_MATCH:
        outp.write("The print statement in roll_off is incorrect for the first player.\n")
        outp.write("Do not forget to add the handicap.\n")
        score -= 0.25
        if not step:
            return (FAIL_INCORRECT, max(0,score))
    elif error == PRINT_SECND_MATCH:
        outp.write("The print statement in roll_off is incorrect for the second player.\n")
        outp.write("Do not forget to add the handicap.\n")
        score -= 0.25
        if not step:
            return (FAIL_INCORRECT, max(0,score))
    
    if result is None:
        outp.write('Function roll_off is missing a return statement.\n')
        score -= 0.25
        if not step:
            return (FAIL_INCORRECT, max(0,score))
    if result:
        outp.write('Function roll_off returns the wrong value.\n')
        score -= 0.25
        if not step:
            return (FAIL_INCORRECT, max(0,score))
    
    env.reset()
    PLAYER1 = -5
    PLAYER2 = 5
    
    try:
        result = env.module.roll_off(PLAYER1,PLAYER2)
    except:
        result = None
        outp.write("Function roll_off has a major syntax error.\n")
        outp.write(traceback.format_exc(0))
        return (FAIL_CRASHES,0)
    
    error = check_print(env,1,11)
    if error == PRINT_WRONG_LINES:
        outp.write("Function roll_off has the wrong number of print statements: either more than one, or none [2nd Attempt].\n")
        score -= 0.2
        if not step:
            return (FAIL_INCORRECT, max(0,score))
    elif error == PRINT_NO_PERIOD:
        outp.write("The print statement in roll_off is missing a period [2nd Attempt].\n")
        score -= 0.05
        if not step:
            return (FAIL_INCORRECT, max(0,score))
    elif error == PRINT_FIRST_MATCH:
        outp.write("The print statement in roll_off is incorrect for the first player [2nd Attempt].\n")
        outp.write("Do not forget to add the handicap.\n")
        score -= 0.25
        if not step:
            return (FAIL_INCORRECT, max(0,score))
    elif error == PRINT_SECND_MATCH:
        outp.write("The print statement in roll_off is incorrect for the second player [2nd Attempt].\n")
        outp.write("Do not forget to add the handicap.\n")
        score -= 0.25
        if not step:
            return (FAIL_INCORRECT, max(0,score))
    
    if result is None:
        outp.write('Function roll_off uses if-statements.\n')
        score -= 0.25
        if not step:
            return (FAIL_INCORRECT, max(0,score))
    if result:
        outp.write('Function roll_off returns the wrong value [2nd Attempt].\n')
        score -= 0.25
        if not step:
            return (FAIL_INCORRECT, max(0,score))
    
    env.reset()
    PLAYER1 = 5
    PLAYER2 = -5
    
    try:
        result = env.module.roll_off(PLAYER1,PLAYER2)
    except:
        result = None
        outp.write("Function roll_off has a major syntax error.\n")
        outp.write(traceback.format_exc(0))
        return (PRINT_CRASHES,0)
    
    error = check_print(env,12,3)
    if error == PRINT_WRONG_LINES:
        outp.write("Function roll_off has the wrong number of print statements: either more than one, or none [3rd Attempt].\n")
        score -= 0.2
        if not step:
            return (FAIL_INCORRECT, max(0,score))
    elif error == PRINT_NO_PERIOD:
        outp.write("The print statement in roll_off is missing a period [3rd Attempt].\n")
        score -= 0.05
        if not step:
            return (FAIL_INCORRECT, max(0,score))
    elif error == PRINT_FIRST_MATCH:
        outp.write("The print statement in roll_off is incorrect for the first player [3rd Attempt].\n")
        outp.write("Do not forget to add the handicap.\n")
        score -= 0.25
        if not step:
            return (FAIL_INCORRECT, max(0,score))
    elif error == PRINT_SECND_MATCH:
        outp.write("The print statement in roll_off is incorrect for the second player[3rd Attempt].\n")
        outp.write("Do not forget to add the handicap.\n")
        score -= 0.25
        if not step:
            return (FAIL_INCORRECT, max(0,score))
    
    if result is None:
        outp.write('Function roll_off uses if-statements.\n')
        score -= 0.25
        if not step:
            return (FAIL_INCORRECT, max(0,score))
    if not result:
        outp.write('Function roll_off returns the wrong value [3rd Attempt].\n')
        score -= 0.25
        if not step:
            return (FAIL_INCORRECT, max(0,score))
    
    return (TEST_SUCCESS, max(0,score))


def grade_player2(file,step=0,outp=sys.stdout):
    """
    Returns the test result and score for the second player
    
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
    elif not hasattr(env.module,'roll_off'):
        outp.write("File %s is missing the header for roll_off.\n" % repr(file))
        return (FAIL_INCORRECT,0)
    
    code = env.module.roll_off.__code__
    if not 'rollem' in code.co_names:
        outp.write("Function roll_off does not call rollem as a helper.\n")
        score -= 0.5
        if not step:
            return (FAIL_INCORRECT, max(0,score))
    if 'random' in code.co_names or 'randint' in code.co_names:
        outp.write("Function roll_off is still calling the function randint (which should be removed).\n")
        score -= 0.5
        if not step:
            return (FAIL_INCORRECT, max(0,score))
    if 'die1' in code.co_varnames or 'die2' in code.co_varnames:
        outp.write("Function roll_off still has the local variables 'die1' and 'die2'.\n")
        score -= 0.2
        if not step:
            return (FAIL_INCORRECT, max(0,score))
    
    import random
    random.seed(10)
    
    PLAYER1 = 0
    PLAYER2 = 0
    
    try:
        result = env.module.roll_off(PLAYER1,PLAYER2)
    except:
        result = None
        outp.write("Function roll_off has a major syntax error.\n")
        outp.write(traceback.format_exc(0))
        return (FAIL_CRASHES,0)
    
    error = check_print(env,6,8)
    if error == PRINT_WRONG_LINES:
        outp.write("Function roll_off has the wrong number of print statements: either more than one, or none.\n")
        score -= 0.2
        if not step:
            return (FAIL_INCORRECT, max(0,score))
    elif error == PRINT_NO_PERIOD:
        outp.write("The print statement in roll_off is missing a period.\n")
        score -= 0.05
        if not step:
            return (FAIL_INCORRECT, max(0,score))
    elif error == PRINT_FIRST_MATCH:
        outp.write("The print statement in roll_off is incorrect for the first player.\n")
        outp.write("Do not forget to add the handicap.\n")
        score -= 0.25
        if not step:
            return (FAIL_INCORRECT, max(0,score))
    elif error == PRINT_SECND_MATCH:
        outp.write("The print statement in roll_off is incorrect for the second player.\n")
        outp.write("Do not forget to add the handicap.\n")
        score -= 0.25
        if not step:
            return (FAIL_INCORRECT, max(0,score))
    
    if result is None:
        outp.write('Function roll_off is missing a return statement.\n')
        score -= 0.25
        if not step:
            return (FAIL_INCORRECT, max(0,score))
    if result:
        outp.write('Function roll_off returns the wrong value.\n')
        score -= 0.25
        if not step:
            return (FAIL_INCORRECT, max(0,score))
    
    env.reset()
    PLAYER1 = -5
    PLAYER2 = 5
    
    try:
        result = env.module.roll_off(PLAYER1,PLAYER2)
    except:
        result = None
        outp.write("Function roll_off has a major syntax error.\n")
        outp.write(traceback.format_exc(0))
        return (FAIL_CRASHES,0)
    
    error = check_print(env,1,11)
    if error == PRINT_WRONG_LINES:
        outp.write("Function roll_off has the wrong number of print statements: either more than one, or none [2nd Attempt].\n")
        score -= 0.2
        if not step:
            return (FAIL_INCORRECT, max(0,score))
    elif error == PRINT_NO_PERIOD:
        outp.write("The print statement in roll_off is missing a period [2nd Attempt].\n")
        score -= 0.05
        if not step:
            return (FAIL_INCORRECT, max(0,score))
    elif error == PRINT_FIRST_MATCH:
        outp.write("The print statement in roll_off is incorrect for the first player [2nd Attempt].\n")
        outp.write("Do not forget to add the handicap.\n")
        score -= 0.25
        if not step:
            return (FAIL_INCORRECT, max(0,score))
    elif error == PRINT_SECND_MATCH:
        outp.write("The print statement in roll_off is incorrect for the second player [2nd Attempt].\n")
        outp.write("Do not forget to add the handicap.\n")
        score -= 0.25
        if not step:
            return (FAIL_INCORRECT, max(0,score))
    
    if result is None:
        outp.write('Function roll_off uses if-statements.\n')
        score -= 0.25
        if not step:
            return (FAIL_INCORRECT, max(0,score))
    if result:
        outp.write('Function roll_off returns the wrong value [2nd Attempt].\n')
        score -= 0.25
        if not step:
            return (FAIL_INCORRECT, max(0,score))
    
    env.reset()
    PLAYER1 = 5
    PLAYER2 = -5
    
    try:
        result = env.module.roll_off(PLAYER1,PLAYER2)
    except:
        result = None
        outp.write("Function roll_off has a major syntax error.\n")
        outp.write(traceback.format_exc(0))
        return (FAIL_CRASHES,0)
    
    error = check_print(env,12,3)
    if error == PRINT_WRONG_LINES:
        outp.write("Function roll_off has the wrong number of print statements: either more than one, or none [3rd Attempt].\n")
        score -= 0.2
        if not step:
            return (FAIL_INCORRECT, max(0,score))
    elif error == PRINT_NO_PERIOD:
        outp.write("The print statement in roll_off is missing a period [3rd Attempt].\n")
        score -= 0.05
        if not step:
            return (FAIL_INCORRECT, max(0,score))
    elif error == PRINT_FIRST_MATCH:
        outp.write("The print statement in roll_off is incorrect for the first player [3rd Attempt].\n")
        outp.write("Do not forget to add the handicap.\n")
        score -= 0.25
        if not step:
            return (FAIL_INCORRECT, max(0,score))
    elif error == PRINT_SECND_MATCH:
        outp.write("The print statement in roll_off is incorrect for the second player [3rd Attempt].\n")
        outp.write("Do not forget to add the handicap.\n")
        score -= 0.25
        if not step:
            return (FAIL_INCORRECT, max(0,score))
    
    if result is None:
        outp.write('Function roll_off uses if-statements.\n')
        score -= 0.25
        if not step:
            return (FAIL_INCORRECT, max(0,score))
    if not result:
        outp.write('Function roll_off returns the wrong value [3rd Attempt].\n')
        score -= 0.25
        if not step:
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
    outp.write('Helper function comments:\n')
    status, p1 = grade_helper(file,1,outp)
    if p1 == 1:
        outp.write('The helper functions looks good.\n\n')
    else:
        outp.write('\n')
    
    if not status:
        outp.write('Player 1 comments:\n')
        status, p2 = grade_player1(file,1,outp)
        if p2 == 1:
            outp.write('The code for player 1 looks good.\n\n')
        else:
            outp.write('\n')
    else:
        p2 = 0
    
    if not status:
        outp.write('Player 2 comments:\n')
        status, p3 = grade_player2(file,1,outp)
        if p3 == 1:
            outp.write('The code for player 2 looks good.\n\n')
        else:
            outp.write('\n')
    else:
        p3 = 0
    
    total = round(0.2*p1+0.4*p2+0.4*p3,3)
    return total


def grade(outp=sys.stdout):
    """
    Invokes this subgrader (returning a percentage)
    """
    return grade_file('game.py',outp)


if __name__ == '__main__':
    print(grade())
