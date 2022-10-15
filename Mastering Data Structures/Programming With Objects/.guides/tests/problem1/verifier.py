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


def grade_script(file,step=0,outp=sys.stdout):
    """
    Returns the test result and score for the script code
    
    The step parameter is the phase in the grading pass.  Step 0 checks that green
    object was created.  Step 1 checks that the red object was created.  Step 2
    checks that the brown object was created.  Step 3 verifies that what was green
    is now brown. Steps 0-4 will stop at the first error found.  Otherwise 
    it will continue through and try to find all errors.
    
    Parameter file: The file name
    Precondition: file is a string of a file in the given workspace
    
    Parameter step: The current verfication/grading step
    Precondition: step is 0 -4
    
    Parameter outp: The output stream
    Precondition: outp is a stream writer
    """
    score = 1
    env  = import_module(file)
    code = parse_file(file)
    if type(env) == str:
        outp.write(env)
        return (FAIL_CRASHES, 0)
    
    calls = set()
    for item in ast.walk(code):
        if type(item) == ast.Call:
            if type(item.func) == ast.Attribute:
                calls.add(item.func.attr)
            elif type(item.func) == ast.Name:
                calls.add(item.func.id)
    
    green = introcs.RGB(0,255,0)
    if not hasattr(env.module,'green'):
        outp.write("File %s does not have a variable called 'green'.\n" % repr(file))
        score -= 0.2
        if step < 4:
            return (FAIL_INCORRECT,max(0,score))
    elif step < 3 and env.module.green != green:
        outp.write("Variable 'green' is not assigned to the correct value [Expected %s, got %s].\n" % (repr(green),repr(env.module.green)))
        score -= 0.15
        if step < 4:
            return (FAIL_INCORRECT,max(0,score))
    else:
        if len(env.printed) < 1 or not (repr(green) in env.printed[0] or str(green) in env.printed[0]):
            outp.write("The value 'green' is not the first print statment.\n")
            score -= 0.05
            if step < 4:
                return (FAIL_INCORRECT,max(0,score))
    
    if step:
        red = introcs.RGB(255,0,0,128)
        if not hasattr(env.module,'red'):
            outp.write("File %s does not have a variable called 'red'.\n" % repr(file))
            score -= 0.2
            if step < 4:
                return (FAIL_INCORRECT,max(0,score))
        elif env.module.red != red:
            outp.write("Variable 'red' is not assigned to the correct value [Expected %s, got %s].\n" % (repr(red),repr(env.module.red)))
            score -= 0.15
            if step < 4:
                return (FAIL_INCORRECT,max(0,score))
        else:
            if len(env.printed) < 2 or not (repr(red) in env.printed[1] or str(red) in env.printed[1]):
                outp.write("The value 'red' is not the second print statment.\n")
                score -= 0.05
                if step < 4:
                    return (FAIL_INCORRECT,max(0,score))
    
    if step > 1:
        brown = introcs.RGB(128,127,0)
        if not hasattr(env.module,'brown'):
            outp.write("File %s does not have a variable called 'brown'.\n" % repr(file))
            score -= 0.2
            if step < 4:
                return (FAIL_INCORRECT,max(0,score))
        elif env.module.brown != brown:
            outp.write("Variable 'brown' is not assigned to the correct value [Expected %s, got %s].\n" % (repr(brown),repr(env.module.brown)))
            score -= 0.15
            if step < 4:
                return (FAIL_INCORRECT,max(0,score))
        elif not 'blend' in calls:
            outp.write("The script code does not call the function 'blend'.\n")
            score -= 0.1
            if step < 4:
                return (FAIL_INCORRECT,max(0,score))
        else:
            if len(env.printed) < 3 or not (repr(brown) in env.printed[2] or str(brown) in env.printed[2]):
                outp.write("The value 'brown' is not the third print statment.\n")
                score -= 0.05
                if step < 4:
                    return (FAIL_INCORRECT,max(0,score))
    
    if step > 2:
        green = introcs.RGB(128,127,0)
        if env.module.green != green:
            outp.write("The script code does not modify 'green' correctly [Expected %s, got %s].\n" % (repr(green),repr(env.module.green)))
            score -= 0.15
            if step < 4:
                return (FAIL_INCORRECT,max(0,score))
        elif not 'blendUnder' in calls:
            outp.write("The script code does not call the function 'blendUnder'.\n")
            score -= 0.1
            if step < 4:
                return (FAIL_INCORRECT,max(0,score))
        else:
            if len(env.printed) < 4 or not (repr(green) in env.printed[3] or str(green) in env.printed[3]):
                outp.write("The value 'green' is not the fourth print statment.\n")
                score -= 0.05
                if step < 4:
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
        outp.write('Script code comments:\n')
        status, p2 = grade_script(file,4,outp)
        if p2 == 1:
            outp.write('The script code looks good.\n\n')
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
    return grade_file('script.py',outp)


if __name__ == '__main__':
    print(grade())