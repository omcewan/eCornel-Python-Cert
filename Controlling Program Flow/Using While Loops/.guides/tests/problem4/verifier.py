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
import random
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


WORKSPACE = [os.path.expanduser('~'),'workspace','exercise4']
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
    
    Parameter values: The input values to use
    Precondition: values is a tuple of strings
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


def grade_bet(file,step=0,outp=sys.stdout):
    """
    Returns the test result and score for the implementation of get_bet
    
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
    
    function = 'get_bet'
    testcase = [(1000,500),(800,'a','b12','20a',200),(800,-200,0,300),(800,120.5,120.0,300),(300,500,600,100)]
    env = import_module(file)
    
    if type(env) == str:
        outp.write(env)
        return (FAIL_CRASHES, 0)
    elif env.printed != []:
        outp.write("File %s is missing \"if __name__ == '__main__'\" before script code.\n" % repr(file))
        return (FAIL_CRASHES, 0)
    elif not hasattr(env.module,function):
        outp.write("File %s is missing the header for %s.\n" % (repr(file),repr(function)))
        return (FAIL_INCORRECT, 0)
    elif not hasattr(env.module,'__whileguard__'):
        outp.write("File %s was not properly processed by the autograder.\n" % repr(file))
        return (FAIL_INCORRECT, 0)
    
    func = getattr(env.module,function)
    values = (800,'a',-200,1000,120.5,100)
    args = values[0]
    try:
        env.reset()
        env.revalue(*values[1:])
        expected = values[-1]
        received = func(values[0])
        if env.inputed == []:
            outp.write("The function %s did not prompt for any input.\n" % repr(function))
            return (FAIL_INCORRECT, 0)
        elif env.module.__whileguard__ >= env.LIMIT:
            data = ', '.join(map(str,values[1:]))
            outp.write("The function %s has an infinite loop on the following input: %s.\n" % (repr(function),data))
            outp.write("Stopped loop after %d iterations.\n" % env.module.__whileguard__)
            score -= .15
            if not step:
                return (FAIL_INCORRECT,max(0,score))
        else:
            first = env.inputed[0]
            right = "Make a bet: "
            if first.strip() != right.strip():
                outp.write("The function %s does not prompt with %s.\n" % (repr(function),repr(right)))
                score -= 0.1
                if not step:
                    return (FAIL_INCORRECT,max(0,score))
            elif first != right:
                outp.write("The prompt in function %s does not have a single space after the ':'.\n" % repr(function))
                score -= 0.05
                if not step:
                    return (FAIL_INCORRECT,max(0,score))
            else:
                pos = 0
                match = True
                while pos < len(env.inputed) and match:
                    item = env.inputed[pos]
                    pos += 1
                    if item != first:
                        match = False
                
                if not match:
                    outp.write("The function %s has more than one call to 'input'.\n" % repr(function))
                    score -= 0.1
                    match = False
                    if not step:
                        return (FAIL_INCORRECT,max(0,score))
    except:
        import traceback
        data = ', '.join(map(str,values[1:]))
        outp.write("The call %s(%d) crashed on the following input: %s.\n" % (function,args,data))
        outp.write(traceback.format_exc(0)+'\n')
        score -= 1/len(testcase)
        if not step:
            return (FAIL_INCORRECT,max(0,score))
    
    
    for values in testcase:
        args = values[0]
        try:
            env.reset()
            env.revalue(*tuple(values[1:]))
            expected = values[-1]
            received = func(values[0])
            
            if env.inputed == []:
                outp.write("The function %s did not prompt for any input.\n" % repr(function))
                return (FAIL_INCORRECT, 0)
            elif env.module.__whileguard__ >= env.LIMIT:
                data = ', '.join(map(str,values[1:]))
                outp.write("The function %s has an infinite loop on the following input: %s.\n" % (repr(function),data))
                outp.write("Stopped loop after %d iterations.\n" % env.module.__whileguard__)
                score -= 1/len(testcase)
                if not step:
                    return (FAIL_INCORRECT,max(0,score))
            else:
                if len(values[1:]) > 1 and env.printed == []:
                    outp.write("The function %s did not print any error messages.\n" % repr(function))
                    score -= 0.5
                    if not step:
                        return (FAIL_INCORRECT,max(0,score))
                elif len(values[1:]) > 1:
                    for pos in range(len(values[1:-1])):
                        item = values[pos+1]
                        if type(item) != int:
                            correct = "The bet must be an integer."
                        elif item <= 0:
                            correct = 'The bet must be a positive integer.'
                        elif item > values[0]:
                            correct = 'You do not have enough credits for that bet.'
                        given = env.printed[pos].strip() if pos < len(env.printed) else ''
                        if correct != given:
                            outp.write("The call %s(%d) did not display %s on the following input: '%s'.\n" % (function,args,repr(correct),str(item)))
                            score -= 0.05
                            if not step:
                                return (FAIL_INCORRECT,max(0,score))
                
                if received != expected:
                    outp.write("The call %s(%d) returned %d, not %d., on the following input: %s\n" % (function, args, received, expected, str(expected)))
                    score -= 1/len(testcase)
                    if not step:
                        return (FAIL_INCORRECT,max(0,score))
        except:
            inputs = tuple(map(str,values[1:]))
            import traceback
            data = ', '.join(map(str,values[1:]))
            outp.write("The call %s(%d) crashed on the following input: %s.\n" % (function,args,data))
            outp.write(traceback.format_exc(0)+'\n')
            score -= 1/len(testcase)
            if not step:
                return (FAIL_INCORRECT,max(0,score))
    
    return (TEST_SUCCESS,max(0,score))


def grade_session(file,step=0,outp=sys.stdout):
    """
    Returns the test result and score for the implementation of session
    
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
    
    function = 'session'
    env = import_module(file)
    
    if type(env) == str:
        outp.write(env)
        return (FAIL_CRASHES, 0)
    elif env.printed != []:
        outp.write("File %s is missing \"if __name__ == '__main__'\" before script code.\n" % repr(file))
        return (FAIL_CRASHES, 0)
    elif not hasattr(env.module,function):
        outp.write("File %s is missing the header for %s.\n" % (repr(file),repr(function)))
        return (FAIL_INCORRECT, 0)
    elif not hasattr(env.module,'__whileguard__'):
        outp.write("File %s was not properly processed by the autograder.\n" % repr(file))
        return (FAIL_INCORRECT, 0)
    
    sessions = [(0, 100, 7, 'a', 14, 's', -100),
                (8, 500, 4, 'b', 10, 'a', 17, 's', 0),
                (50, 300, 8, 'a', 14, 'b', 20, 300),
                (60, 300, 5, 'b', 10, 'b', 13, 'a', 19, 's', 150),
                (60, 100, 5, 'b', 10, 'b', 13, 'a', 19, 'a', 24, -100),
                (90, 250, 4, 'b', 6, 'b', 14, 'a', 20, 250),
                (120, 50, 4, 'b', 8, 'a', 15, 's', -38),
                (128, 300, 4, 'b', 11, 'a', 17, 's', 0),
                (138, 100, 4, 'b', 11, 'a', 18, 's', 25),
                (500, 500, 8, 'a', 15, 'a', 21, -500),
                (575, 400, 5, 'a', 9, 'b', 16, 's', -200),
                (600, 200, 5, 'b', 11, 'b', 19, 's', 100),
                (1234, 200, 8, 'a', 12, 'b', 13, 'b', 15, 'b', 16, 'b', 18, 's', 50),
                (2578, 400, 8, 'a', 13, 'a', 18, 's', 100),
                (3337, 200, 3, 'b', 4, 'b', 8, 'a', 13, 'b', 20, 200),
                (4441, 300, 8, 'a', 14, 'b', 19, 's', 150),
                (4445, 50, 2, 's', -50),
                (4445, 100, 2, 'a', 9, 'b', 15, 's', -75),
                (5659, 100, 5, 'b', 8, 'a', 13, 'b', 21, -100),
                (7774, 250, 2, 'b', 10, 'a', 16, 's', -125)]
    
    func = getattr(env.module,function)
    values = ('a','c','3','A','b','1','b','x','b','d','B','b','s')
    seed = 1234
    args = 200
    try:
        random.seed(seed)
        env.reset()
        env.revalue(*values)
        received = func(args)
        expected = 50
        
        if env.inputed == []:
            outp.write("The call %s(%d) did not prompt for any input.\n" % (function,args))
            return (FAIL_INCORRECT, 0)
        elif env.module.__whileguard__ >= env.LIMIT:
            data = ', '.join(map(str,values))
            outp.write("The call %s(%d) has an infinite loop.\n" % (function,args))
            outp.write("Stopped loop after %d iterations.\n" % env.module.__whileguard__)
            outp.write("Test %s with random seed %d and the following input: %s.\n\n" % (repr(function),seed,data))
            score -= .35
            if not step:
                return (FAIL_INCORRECT,max(0,score))
        else:
            retry = False
            first = env.inputed[0]
            right = "Choose (a) 4-7, (b) 1-8, or (s)top: "
            if first.strip() != right.strip():
                outp.write("The function %s does not prompt with %s.\n" % (repr(function),repr(right)))
                score -= 0.1
                retry = True
            elif first != right:
                outp.write("The prompt in function %s does not have a single space after the ':'.\n" % repr(function))
                score -= 0.05
                retry = True
            else:
                pos = 0
                match = True
                while pos < len(env.inputed) and match:
                    item = env.inputed[pos]
                    pos += 1
                    if item != first:
                        match = False
                
                if not match:
                    outp.write("The function %s has more than one call to 'prompt'.\n" % repr(function))
                    score -= 0.1
                    match = False
                    retry = True
            
            if len(env.printed) == 0:
                outp.write("The call %s(%d) does not display any output.\n" % (function,args))
                score -= 0.25
                retry = True
            else:
                correct = 'Your score is '
                anerror = 'Invalid option. Choose one of '
                first = env.printed[0]
                
                pos2 = 1
                want = '8'
                if not want in first and not 'score' in first:
                    outp.write("The call %s(%d) does not display the score at the start.\n" % (function,args))
                    pos2 = 0
                    score -= 0.1
                    retry = True
                elif not first.startswith(correct):
                    outp.write("The call %s(%d) does not display the score with the prefix %s.\n" % (function,args,repr(correct)))
                    score -= 0.05
                    retry = True
                elif not want in first:
                    outp.write("The call %s(%d) not does display the correct score at start [expected %s].\n" % (function,args,want))
                    score -= 0.05
                    retry = True
                elif not first.startswith(correct+want):
                    outp.write("The call %s(%d) not does format the score properly [wanted '%s'].\n" % (function,args,correct+want))
                    score -= 0.05
                    retry = True
            
            match1 = True
            match2 = True
            match3 = True
            for pos1 in range(len(values)):
                if values[pos1] in ('a','b'):
                    if len(env.printed) <= pos2 or not env.printed[pos2].startswith(correct):
                        match = False
                    pos2 += 1
                elif values[pos1] != 's':
                    if len(env.printed) <= pos2 or not env.printed[pos2].startswith(anerror):
                        match2 = False
                    if len(env.printed) <= pos2+1 or env.printed[pos2+1] != '':
                        match2 = False
                    pos2 += 2
                else:
                    if pos2 < len(env.printed) and env.printed[pos2].startswith(correct):
                        match3 = False
            
            if not match1:
                outp.write("The function %s does not redisplay the score after valid input.\n" % repr(function))
                score -= 0.1
                match = False
                retry = True
            
            if not match2:
                outp.write("The function %s does not call 'prompt' properly.\n" % repr(function))
                score -= 0.1
                match = False
                retry = True
            
            if not match3:
                outp.write("The function %s redisplays the score after standing (it should not).\n" % repr(function))
                score -= 0.05
                match = False
                retry = True
            
            if retry:
                data = ', '.join(map(str,values))
                outp.write("Test %s with random seed %d and the following input: %s.\n\n" % (repr(function),seed,data))
                if not step:
                    return (FAIL_INCORRECT,max(0,score))
            
    except:
        import traceback
        data = ', '.join(map(str,values))
        outp.write("The call %s(%d) crashed.\n" % (function,args))
        outp.write(traceback.format_exc(0)+'\n')
        outp.write("Test %s with random seed %d and the following input: %s.\n\n" % (repr(function),seed,data))
        score -= .35
        if not step:
            return (FAIL_INCORRECT,max(0,score))    
    
    for play in sessions:
        seed = play[0]
        args = play[1]
        values = play[3:-1:2]
        scores = play[2:-1:2]
        random.seed(seed)
        try:
            env.reset()
            env.revalue(*values)
            expected = play[-1]
            received = func(args)
            
            if env.inputed == []:
                outp.write("The call %s(%d) did not prompt for any input.\n" % (function,args))
                return (FAIL_INCORRECT, 0)
            elif env.module.__whileguard__ >= env.LIMIT:
                data = ', '.join(map(str,values))
                outp.write("The call %s(%d) has an infinite loop.\n" % (function,args))
                outp.write("Stopped loop after %d iterations.\n" % env.module.__whileguard__)
                outp.write("Test %s with random seed %d and the following input: %s.\n\n" % (repr(function),seed,data))
                score -= 1/len(sessions)
                if not step:
                    return (FAIL_INCORRECT,max(0,score))
            else:
                match = True
                for pos in range(len(values)):
                    want = ' '+str(scores[pos])
                    have =  env.printed[pos]
                    have = have[have.rfind(' '):].strip()
                    if not have[-1].isdigit():
                        have = have[:-1]
                    
                    round = 'at the start' if pos == 0 else 'after round '+str(pos)
                    
                    if not want in env.printed[pos]:
                        outp.write('The session does not display the correct score %s [expected%s, received %s].\n' % (round,want,have))
                        score -= 0.2/len(sessions)
                        match = False
                
                final = play[-3] if play[-2] == 's' else play[-2]
                if final >= 18 and final <= 20 and not env.printed[-1].startswith('You won '):
                    outp.write("The call %s(%d) does not display the payout at the end.\n" % (function,args))
                    score -= 0.1/len(sessions)
                    match = False
                elif final == 17 and env.printed[-1].startswith('You lost '):
                    outp.write("The call %s(%d) incorrectly marks a gain of 0 as a loss.\n" % (function,args))
                    score -= 0.1/len(sessions)
                    match = False
                elif final == 17 and not env.printed[-1].startswith('You won '):
                    outp.write("The call %s(%d) does not display the payout at the end.\n" % (function,args))
                    score -= 0.1/len(sessions)
                    match = False
                elif (final < 17 or final > 20) and not env.printed[-1].startswith('You lost '):
                    outp.write("The call %s(%d) does not the display payout at the end.\n" % (function,args))
                    score -= 0.1/len(sessions)
                    match = False
                elif not str(abs(received)) in env.printed[-1]:
                    outp.write("The call %s(%d) does not display the correct payout at the end.\n" % (function,args))
                    score -= 0.1/len(sessions)
                    match = False
                elif not 'credits' in env.printed[-1]:
                    outp.write("The call %s(%d) does not display the payout in credits.\n" % (function,args))
                    score -= 0.1/len(sessions)
                    match = False
                
                if final == 20:
                    if not env.printed[-2].startswith('Quasar'):
                        outp.write("The call %s(%d) does not display 'Quasar!', before the winnings, on a score of 20.\n" % (repr(function),args))
                        score -= 0.1/len(sessions)
                        match = False
                elif final > 20:
                    if not env.printed[-2].startswith('You busted'):
                        outp.write("The call %s(%d) does not display 'You busted.', before the winnings, when over 20.\n" % (repr(function),args))
                        score -= 0.1/len(sessions)
                        match = False
                
                if received != expected:
                    outp.write("The function %s(%d) returned %d, not %d as expected.\n" % (function, args, received, expected))
                    score -= 1/len(sessions)
                    match = False
                
                if not match:
                    data = ', '.join(map(str,values))
                    outp.write("Test %s with random seed %d and the following input: %s.\n\n" % (repr(function),seed,data))
                    if not step:
                        return (FAIL_INCORRECT,max(0,score))
        except:
            import traceback
            data = ', '.join(map(str,values))
            outp.write("The call %s(%d) crashed.\n" % (function,args))
            outp.write(traceback.format_exc(0)+'\n')
            outp.write("Test %s with random seed %d and the following input: %s.\n\n" % (repr(function),seed,data))
            score -= 1/len(sessions)
            if not step:
                return (FAIL_INCORRECT,max(0,score))
    
    return (TEST_SUCCESS,max(0,score))


def grade_play(file,step=0,outp=sys.stdout):
    """
    Returns the test result and score for the implementation of play
    
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
    
    function = 'play'
    env = import_module(file)
    
    if type(env) == str:
        outp.write(env)
        return (FAIL_CRASHES, 0)
    elif env.printed != []:
        outp.write("File %s is missing \"if __name__ == '__main__'\" before script code.\n" % repr(file))
        return (FAIL_CRASHES, 0)
    elif not hasattr(env.module,function):
        outp.write("File %s is missing the header for %s.\n" % (repr(file),repr(function)))
        return (FAIL_INCORRECT, 0)
    elif not hasattr(env.module,'__whileguard__'):
        outp.write("File %s was not properly processed by the autograder.\n" % repr(file))
        return (FAIL_INCORRECT, 0)
    
    playthru =[ ( 50, 1000, (300,'a','b','p'), (300,)),
                ( 50,  200, (200,'b','b','a'), (-200,)),
                (150,  400, (200,'b','a','b','c',200,'b','a','b'), (-200,-200)),
                (100,  500, 
                    (300,'b','a','b','c',200,'a','b','c',400,'a','b','a','b','c',800,'b','b','a','b'),
                    (-300,200,400,-800)),
                ( 50, 2000, 
                    (300,'a','b','c',200,'a','b','s','c',200,'a','a','a','b','c',500,'b','a','b','c',300,'a','a','b','b','p'),
                    (300,0,200,500,-300))]
    
    func = getattr(env.module,function)
    seed = 50
    args = 100
    values = (50,'a','b','s','P','p')
    scores = (50,)
    try:
        random.seed(seed)
        env.reset()
        env.revalue(*values)
        func(args)
        if env.inputed == []:
            outp.write("The call %s(%d) did not prompt for any input.\n" % (function,args))
            return (FAIL_INCORRECT, 0)
        if env.printed == []:
            outp.write("The call %s(%d) did not display any output.\n" % (function,args))
            return (FAIL_INCORRECT, 0)
        elif env.module.__whileguard__ >= env.LIMIT:
            data = ', '.join(map(str,values))
            outp.write("The call %s(%d) has an infinite loop.\n" % (function,args))
            outp.write("Stopped loop after %d iterations.\n" % env.module.__whileguard__)
            outp.write("Test %s with random seed %d and the following input: %s.\n\n" % (repr(function),seed,data))
            score -= 0.4
            if not step:
                return (FAIL_INCORRECT,max(0,score))
        else:
            retry = False
            
            if not env.printed[0].startswith('You have '):
                outp.write("The call %s(%d) does not display the credits at the start.\n" % (function,args))
                score -= 0.15
                retry = True
            elif not str(args) in env.printed[0]:
                outp.write("The call %s(%d) does not display the correct number of credits at the start.\n" % (function,args))
                score -= 0.15
                retry = True
            elif not 'credits' in env.printed[0]:
                outp.write("The call %s(%d) does not display the starting score in credits.\n" % (function,args))
                score -= 0.15
                retry = True
            
            pos = 0
            found = False
            while pos < len(env.printed) and not found:
                line = env.printed[pos]
                if line.startswith('You won') or line.startswith('You lost'):
                    found = True
                pos += 1
            
            if len(env.printed) <= pos or not env.printed[pos].startswith('You have '):
                outp.write("The call %s(%d) does not display the credits after each session.\n" % (function,args))
                score -= 0.1
                retry = True
            elif not str(args+scores[0]) in env.printed[pos]:
                outp.write("The call %s(%d) does not display the correct number of credits after each session.\n" % (function,args))
                score -= 0.1
                retry = True
            
            other = None
            first = None
            secnd = None
            third = None
            correct = 'Do you want to (c)ontinue or (p)ayout? '
            for item in env.inputed:
                if item.startswith('Make a bet'):
                    if first is None:
                        first = item
                    elif first != item:
                        other = item
                elif item.startswith('Choose (a)'):
                    if secnd is None:
                        secnd = item
                    elif secnd != item:
                        other = item
                elif item.startswith(correct[:6]):
                    if third is None:
                        third = item
                    elif third != item:
                        other = item
                else:
                    other = item
            
            if not other is None:
                outp.write("The call %s(%d) has an incorrect input prompt %s.\n" % (function,args,repr(other)))
                score -= 0.05
                retry = True
            
            if third.strip() != correct.strip():
                outp.write("The function %s does not prompt with %s after a session.\n" % (repr(function),repr(correct)))
                score -= 0.1
                retry = True
            elif third != correct:
                outp.write("The prompt in function %s does not have a single space after the '?'.\n" % repr(function))
                score -= 0.05
                retry = True
            
            if not env.printed[-1].startswith('You leave with '):
                outp.write("The call %s(%d) does not display 'You leave with X credits.' upon ending the game.\n" % (function,args))
                score -= 0.1
                retry = True
            elif not str(args+scores[0]) in env.printed[-1]:
                outp.write("The call %s(%d) does not display the correct number of credits upon ending the game.\n" % (function,args))
                score -= 0.1
                retry = True
            
            if retry:
                data = ', '.join(map(str,values))
                outp.write("Test %s with random seed %d and the following input: %s.\n\n" % (repr(function),seed,data))
                if not step:
                    return (FAIL_INCORRECT,max(0,score))
    except:
        import traceback
        data = ', '.join(map(str,values))
        outp.write("The call %s(%d) crashed.\n" % (function,args))
        outp.write(traceback.format_exc(0)+'\n')
        outp.write("Test %s with random seed %d and the following input: %s.\n\n" % (repr(function),seed,data))
        score -= .4
        if not step:
            return (FAIL_INCORRECT,max(0,score))
    
    for game in playthru:
        seed = game[0]
        args = game[1]
        values = game[2]
        scores = game[3]
        random.seed(seed)
        try:
            env.reset()
            env.revalue(*values)
            func(args)
            
            if env.inputed == []:
                outp.write("The call %s(%d) did not prompt for any input.\n" % (function,args))
                return (FAIL_INCORRECT, 0)
            if env.printed == []:
                outp.write("The call %s(%d) did not display any output.\n" % (function,args))
                return (FAIL_INCORRECT, 0)
            elif env.module.__whileguard__ >= env.LIMIT:
                data = ', '.join(map(str,values))
                outp.write("The call %s(%d) has an infinite loop.\n" % (function,args))
                outp.write("Stopped loop after %d iterations.\n" % env.module.__whileguard__)
                outp.write("Test %s with random seed %d and the following input: %s.\n\n" % (repr(function),seed,data))
                score -= 1/len(playthru)
                if not step:
                    return (FAIL_INCORRECT,max(0,score))
            else:
                credits = args + sum(scores)
                if credits == 0:
                    correct = 'You went broke.'
                else:
                    correct = 'You leave with '+str(credits)+' credits.'
                
                if not env.printed[-1].startswith(correct[:-1]):
                    data = ', '.join(map(str,values))
                    outp.write('A game with a final score of %d does not print out %s.\n' % (credits,repr(correct)))
                    outp.write("Test %s with random seed %d and the following input: %s.\n\n" % (repr(function),seed,data))
                    score -= 1/len(playthru)
                    if not step:
                        return (FAIL_INCORRECT,max(0,score))
        except:
            import traceback
            data = ', '.join(map(str,values))
            outp.write("The call %s(%d) crashed.\n" % (function,args))
            outp.write(traceback.format_exc()+'\n')
            outp.write("Test %s with random seed %d and the following input: %s.\n\n" % (repr(function),seed,data))
            score -= 1/len(playthru)
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
    
    func = 'get_bet'
    if not status:
        outp.write("Comments on %s:\n" % repr(func))
        status, p2 = grade_bet(file,1,outp)
        if p2 == 1:
            outp.write('The function looks good.\n\n')
        else:
            outp.write('\n')
    else:
        p2 = 0

    func = 'session'
    if not status:
        outp.write("Comments on %s:\n" % repr(func))
        status, p3 = grade_session(file,1,outp)
        if p3 == 1:
            outp.write('The function looks good.\n\n')
        else:
            outp.write('\n')
    else:
        p3 = 0
    
    func = 'play'
    if not status:
        outp.write("Comments on %s:\n" % repr(func))
        status, p4 = grade_play(file,1,outp)
        if p4 == 1:
            outp.write('The function looks good.\n\n')
        else:
            outp.write('\n')
    else:
        p4 = 0
    
    total = round(0.05*p1+0.25*p2+0.4*p3+0.3*p4,3)
    return total


def grade(outp=sys.stdout):
    """
    Invokes this subgrader (returning a percentage)
    """
    return grade_file('quasar.py',outp)


if __name__ == '__main__':
    print(grade())