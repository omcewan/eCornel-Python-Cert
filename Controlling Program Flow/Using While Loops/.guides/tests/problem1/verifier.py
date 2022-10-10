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


def grade_func(file,step=0,outp=sys.stdout):
    """
    Returns the test result and score for the implementation of count_inputs
    
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
    
    function = 'count_inputs'
    testcase = ['y3y3y0yxn','yn','n','yyyyyn','yyn','yYyn','yNNNNNn']
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
    onetime = True
    for inps in testcase:
        try:
            env.reset()
            env.revalue(*tuple(inps))
            expected = inps.count('y')
            received = func()
            
            if env.inputed == []:
                outp.write("The function %s did not prompt for any input.\n" % repr(function))
                return (FAIL_INCORRECT, 0)
            elif onetime:
                onetime = False
                right = 'Keep going [y/n]? '
                first = env.inputed[0]
                if first.strip() != right.strip():
                    outp.write('The function %s does not prompt with %s.\n' % (repr(function),repr(right)))
                    score -= 0.15
                    if not step:
                        return (FAIL_INCORRECT,max(0,score))
                elif first != right:
                    outp.write("The prompt %s does not have single space after the '?'.\n" % repr(first))
                    score -= 0.05
                    if not step:
                        return (FAIL_INCORRECT,max(0,score))
                
                pos = 0
                match = True
                while pos < len(env.inputed) and match:
                    item = env.inputed[pos]
                    pos += 1
                    if item != first:
                        match = False
                
                if not match:
                    outp.write("The function %s has more than one call to 'input'.\n" % repr(function))
                    score -= 0.15
                    match = False
                    if not step:
                        return (FAIL_INCORRECT,max(0,score))
                
                bads = len(inps)-inps.count('y')-inps.count('n')
                if len(env.printed) == 0:
                    outp.write('The function %s does not print any error messages.\n' % repr(function))
                    score -= 0.2
                    if not step:
                        return (FAIL_INCORRECT,max(0,score))
                else:
                    right = "Answer unclear. Use 'y' or 'n'."
                    first = env.printed[0]
                    if first != right:
                        outp.write('The function %s does not display the error message %s.\n' % (repr(function),repr(right)))
                        score -= 0.15
                        if not step:
                            return (FAIL_INCORRECT,max(0,score))
                    
                    pos = 0
                    match = True
                    while pos < len(env.printed) and match:
                        item = env.printed[pos]
                        pos += 1
                        if item != first:
                            match = False
                    
                    if not match:
                        outp.write("The function %s has more than one error message.\n" % repr(function))
                        score -= 0.15
                        match = False
                        if not step:
                            return (FAIL_INCORRECT,max(0,score))
                    elif len(env.printed) < bads:
                        outp.write('The function %s does not display an error message every time it encounters bad input.\n' % repr(function))
                        score -= 0.15
                        if not step:
                            return (FAIL_INCORRECT,max(0,score))
                    elif len(env.printed) > bads:
                        outp.write('The function %s displays too many error messages.\n' % repr(function))
                        score -= 0.15
                        if not step:
                            return (FAIL_INCORRECT,max(0,score))
            
            data = ', '.join(inps)
            if env.module.__whileguard__ >= env.LIMIT:
                outp.write("The function %s has an infinite loop on the following input: %s.\n" % (repr(function),data))
                outp.write("Stopped loop after %d iterations.\n" % env.module.__whileguard__)
                score -= 1/len(testcase)
                if not step:
                    return (FAIL_INCORRECT,max(0,score))
            elif received != expected:
                outp.write("The function %s returned %d, not %d, for the following input: %s.\n" % (repr(function), received, expected, data))
                score -= 1/len(testcase)
                if not step:
                    return (FAIL_INCORRECT,max(0,score))
        except:
            import traceback
            data = ', '.join(inps)
            outp.write("The function %s crashed on the following input: %s.\n" % (repr(function),data))
            outp.write(traceback.format_exc(0)+'\n')
            score -= 1/len(testcase)
            if not step:
                return (FAIL_INCORRECT,max(0,score))
    
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
    for item in ast.walk(body):
        if type(item) == ast.While:
            found1 = True
        elif type(item) == ast.For:
            found2 = True
    
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
    
    func = 'count_inputs'
    if not crashes:
        outp.write("Function comments:\n")
        status, p2a = grade_func(file,1,outp)
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
    
    total = round(0.05*p1+0.95*p2,3)
    return total


def grade(outp=sys.stdout):
    """
    Invokes this subgrader (returning a percentage)
    """
    return grade_file('counter.py',outp)


if __name__ == '__main__':
    print(grade())