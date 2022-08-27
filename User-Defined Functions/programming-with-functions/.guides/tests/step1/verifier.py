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


WORKSPACE = [os.path.expanduser('~'),'workspace']
#WORKSPACE = ['..']


# Docstrings
DOCSTRING = {'funcs.py': "The functions for the course project", 
             'test.py': "The test script for the course project"}

FUNC_SPECS = {'matching_parens': """
    Returns True if the string s has a matching pair of parentheses.
    
    A matching pair of parentheses is an open parens '(' followed by a closing
    parens ')'.  Any thing can be between the two pair (including other parens).
    
    Example: matching_parens('A (B) C') returns True
    Example: matching_parens('A )B( C') returns False

    Parameter s: The string to check
    Precondition: s is a string (possibly empty)
    """, 
    'first_in_parens' : """
    Returns: The substring of s that is inside the first pair of parentheses.
    
    The first pair of parenthesis consist of the first instance of character
    '(' and the first instance of ')' that follows it.
    
    Example: first_in_parens('A (B) C') returns 'B'
    Example: first_in_parens('A (B) (C)') returns 'B'
    Example: first_in_parens('A ((B) (C))') returns '(B'
    
    Parameter s: a string to check
    Precondition: s is a string with a matching pair of parens '()'.
    """}

PROC_SPECS = { 'test_matching_parens' : "Test procedure for matching_parens",
               'test_first_in_parens' : "Test procedure for first_in_parens"}


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
    
    if file in DOCSTRING:
        if not docs[0].strip().startswith(DOCSTRING[file]):
            outp.write('The docstring for %s does not start with %s.\n' % (repr(file),repr(DOCSTRING[file])))
            score -= 0.3
            if not step:
                return (FAIL_BAD_STYLE,max(0,score))
    
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


def grade_func_headers(file,step=0,outp=sys.stdout):
    """
    Returns the test result and score for the function headers
    
    The step parameter is the phase in the grading pass.  Step 0 verifies the header 
    for matching_parens.  Step 1 verifies the header for first_in_parens.  Steps 0-1
    will stop at the first error found.  Step 2 is the grading pass and will continue 
    through and try to find all errors.
    
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
    elif not hasattr(env.module,'matching_parens'):
        outp.write("File %s is missing the header for 'matching_parens'.\n" % repr(file))
        return (FAIL_INCORRECT, 0)
    elif step and not hasattr(env.module,'first_in_parens'):
        outp.write("File %s is missing the header for 'first_in_parens'.\n" % repr(file))
        return (FAIL_INCORRECT, 0)
    elif not hasattr(env.module,'introcs'):
        outp.write("File %s has not imported the module 'introcs'.\n" % repr(file))
        return (FAIL_INCORRECT, 0)
    
    checks = ['matching_parens','first_in_parens'] if step else ['matching_parens']
    for item in checks:
        func = getattr(env.module,item)
        
        want = 1
        if func.__code__.co_argcount != want:
            found = func.__code__.co_argcount
            outp.write("Function %s has %d parameter%s (expected %d).\n" % (repr(item),found,'' if found == 1 else 's', want))
            score -= 0.2
            if step < 2:
                return (FAIL_INCORRECT, max(0,score))
        
        # Check the specifications
        correct = [ x.strip().lower() for x in FUNC_SPECS[item].split()]
        correct = list(filter(lambda x : len(x) > 0, correct))
        actuals = [ x.strip().lower() for x in func.__doc__.split()]
        actuals = list(filter(lambda x : len(x) > 0, actuals))
        if (correct != actuals):
            outp.write("Function %s does not have the correct docstring.\n" % repr(item))
            score -= 0.4
            if step < 2:
                return (FAIL_INCORRECT, max(0,score))
    
    if len(env.printed) > 0:
        outp.write("File %s contains print statements.\n")
        score -= 0.05
        if step < 2:
            return (FAIL_BAD_STYLE, max(0,score))
    
    return (TEST_SUCCESS, max(0,score))


def grade_proc_headers(file,step=0,outp=sys.stdout):
    """
    Returns the test result and score for the test procedure headers
    
    The step parameter is the phase in the grading pass.  Step 0 verifies the header 
    for test_matching_parens.  Step 1 verifies the header for test_first_in_parens.  
    Steps 0-1 will stop at the first error found.  Step 2 is the grading pass and will 
    continue through and try to find all errors.
    
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
    elif not hasattr(env.module,'test_matching_parens'):
        outp.write("File %s is missing the header for 'test_matching_parens'.\n" % repr(file))
        return (FAIL_INCORRECT, 0)
    elif step and not hasattr(env.module,'test_first_in_parens'):
        outp.write("File %s is missing the header for 'test_first_in_parens'.\n" % repr(file))
        return (FAIL_INCORRECT, 0)
    
    checks = ['test_matching_parens','test_first_in_parens'] if step else ['test_matching_parens']
    for item in checks:
        func = getattr(env.module,item)
        
        want = 0
        if func.__code__.co_argcount != want:
            found = func.__code__.co_argcount
            outp.write("Test procedure %s has %d parameter%s (expected %d).\n" % (repr(item),found,'' if found == 1 else 's', want))
            score -= 0.2
            if step < 2:
                return (FAIL_INCORRECT, max(0,score))
        else:
            env.reset()
            func()
            goal = 'Testing '+item[5:]
            if len(env.printed) == 0:
                outp.write("Test procedure %s does not have a print statement.\n" % repr(item))
                score -= 0.2
                if step < 2:
                    return (FAIL_INCORRECT, max(0,score))
            elif len(env.printed) > 1:
                outp.write("Test procedure %s has more than one print statement.\n" % repr(item))
                score -= 0.2
                if step < 2:
                    return (FAIL_INCORRECT, max(0,score))
            elif not env.printed[0].startswith(goal):
                outp.write("Test procedure %s does not print %s.\n" % (repr(item),repr(goal)))
                score -= 0.2
                if step < 2:
                    return (FAIL_INCORRECT, max(0,score))
        
        # Check the specifications
        correct = PROC_SPECS[item].strip().lower()
        actuals = func.__doc__.strip().lower()
        if (not actuals.startswith(correct)):
            outp.write("Test procedure %s does not have the correct docstring.\n" % repr(item))
            score -= 0.3
            if step < 2:
                return (FAIL_INCORRECT, max(0,score))
        
        env.reset()
    
    
    return (TEST_SUCCESS, max(0,score))



def grade_test_structure(file,step=0,outp=sys.stdout):
    """
    Returns the test result and score for the test script structure
    
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
    text = read_file(file).split('\n')
    code = parse_file(file)
    if type(code) == str:
        outp.write(code)
        return (FAIL_CRASHES, 0)
    elif type(code) != ast.Module:
        outp.write('File %s appears to be corrupted.' % repr(file))
        return (FAIL_CRASHES, 0)
    
    # Crawl to make sure nothing is bad out of body
    body = code.body
    functions = ['print']
    importeds = []
    for pos in range(len(body)):
        if type(body[pos]) == ast.FunctionDef:
            functions.append(body[pos].name)
        elif type(body[pos]) == ast.Import:
            if len(body[pos].names) != 1 or body[pos].names[0].asname:
                outp.write('Nontraditional import at line %d:\n' % body[pos].lineno)
                outp.write(text[body[pos].lineno-1]+'\n')
                outp.write(' '*body[pos].col_offset+'^\n')
                score -= 0.1
                if not step:
                    return (FAIL_BAD_STYLE, max(0,score))
            else:
                importeds.append(body[pos].names[0].name)
        elif type(body[pos]) == ast.ImportFrom:
            outp.write('Nontraditional import at line %d:\n' % body[pos].lineno)
            outp.write(text[body[pos].lineno-1]+'\n')
            outp.write(' '*body[pos].col_offset+'^\n')
            score -= 0.1
            if not step:
                return (FAIL_BAD_STYLE, max(0,score))
        elif type(body[pos]) == ast.Assign:
            outp.write('Unexpected assignment outside of outside of test procedure at line %d:\n' % body[pos].lineno)
            outp.write(text[body[pos].lineno-1]+'\n')
            outp.write(' '*body[pos].col_offset+'^\n')
            score -= 0.1
            if not step:
                return (FAIL_INCORRECT, max(0,score))
        elif type(body[pos]) == ast.Expr:
            if type(body[pos].value) == ast.Str and pos != 0:
                outp.write('Extraneous docstring at line %d:\n' % body[pos].lineno)
                outp.write(text[body[pos].lineno-1]+'\n')
                outp.write(' '*body[pos].col_offset+'^\n')
                score -= 0.05
                if not step:
                    return (FAIL_BAD_STYLE, max(0,score))
        else:
            outp.write('Unexpected Python command outside of test procedure at line %d:\n' % body[pos].lineno)
            outp.write(text[body[pos].lineno-1]+'\n')
            outp.write(' '*body[pos].col_offset+'^\n')
            score -= 0.1
            if not step:
                return (FAIL_INCORRECT, max(0,score))
    
    # Find position of first function def
    start = 0
    while start < len(body) and type(body[start]) != ast.FunctionDef:
        start += 1
    
    if start >= len(body):
        outp.write('File %s has no procedure definitions.' % repr(file))
        return (FAIL_INCORRECT, 0)
    
    # Find the position of the first out of body
    end = start
    while end < len(body) and type(body[end]) == ast.FunctionDef:
        end += 1
    
    if end == len(body):
        outp.write('The following test procedures have not been called: '+', '.join(map(repr,functions[1:]))+'.\n')
        score -= 0.35*len(functions[1:])
        if not step:
            return (FAIL_INCORRECT, max(0,score))
    else:
        called = []
        while end < len(body):
            if type(body[end]) != ast.Expr or type(body[end].value) != ast.Call:
                outp.write('Unexpected Python command outside of test procedure at line %d:\n' % body[end].lineno)
                outp.write(text[body[end].lineno-1]+'\n')
                outp.write(' '*body[end].col_offset+'^\n')
                score -= 0.1
                if not step:
                    return (FAIL_INCORRECT, max(0,score))
            elif not body[end].value.func.id in functions:
                print(body[end].value.func.id)
                print(functions)
                outp.write('Unexpected function call outside of test procedure at line %d:\n' % body[end].lineno)
                outp.write(text[body[end].lineno-1]+'\n')
                outp.write(' '*body[end].col_offset+'^\n')
                score -= 0.1
                if not step:
                    return (FAIL_INCORRECT, max(0,score))
            elif body[end].value.func.id == 'print' and end < len(body)-1:
                outp.write('Unexpected print statement at line %d:\n' % body[end].lineno)
                outp.write("The print 'Module funcs is working correctly' must come last in %s.\n" % repr(file))
                outp.write(text[body[end].lineno-1]+'\n')
                outp.write(' '*body[end].col_offset+'^\n')
                score -= 0.1
                if not step:
                    return (FAIL_INCORRECT, max(0,score))
            elif body[end].value.func.id != 'print':
                called.append(body[end].value.func.id)
            end += 1
        
        if len(called) != len(functions[1:]):
            missing = []
            for item in functions[1:]:
                if not item in called:
                    missing.append(item)
            outp.write('The following test procedures have not been called: '+', '.join(map(repr,missing))+'.\n')
            score -= 0.35*len(missing)
            if not step:
                return (FAIL_INCORRECT, max(0,score))
    
    if type(body[-1]) != ast.Expr or type(body[-1].value) != ast.Call or body[-1].value.func.id != 'print':
        outp.write('File %s does not end with a print statement.\n' % repr(file))
        score -= 0.2
        if not step:
            return (FAIL_INCORRECT, max(0,score))
    else:
        bad = False
        correct = 'Module funcs is working correctly'
        if len(body[-1].value.args) != 1 or type(body[-1].value.args[0]) != ast.Str:
            bad = True
        elif not body[-1].value.args[0].s.startswith(correct):
            bad = True
        if bad:
            outp.write('The final print statement does not show %s.\n' % repr(correct))
            score -= 0.15
            if not step:
                return (FAIL_INCORRECT, max(0,score))
    
    # Check imports
    for mod in ['funcs','introcs']:
        if mod not in importeds:
            outp.write('File %s does not import module %s.\n' % (repr(file),repr(mod)))
            score -= 0.1
            if not step:
                return (FAIL_INCORRECT, max(0,score))
    
    return (TEST_SUCCESS, max(0,score))


pass
#mark -
#mark Graders
def grade(outp=sys.stdout):
    """
    Invokes this subgrader (returning a percentage)
    """
    file = 'funcs.py'
    outp.write("File %s comments:\n" % repr(file))
    status, p1a = grade_docstring(file,1,outp)
    if not status:
        status, p1b = grade_func_headers(file,1,outp)
    else:
        p1b = 0
    p1 = 0.4*p1a+0.6*p1b
    if p1 == 1:
        outp.write('The module %s is structured properly.\n\n' % repr(file))
    else:
        outp.write('\n')
    
    if not status:
        file = 'tests.py'
        outp.write("File %s comments:\n" % repr(file))
        status, p2a = grade_docstring(file,1,outp)
        if not status:
            status, p2b = grade_proc_headers(file,1,outp)
        else:
            p2b = 0
        if not status:
            status, p2c = grade_test_structure(file,1,outp)
        else:
            p2c = 0
        p2 = 0.2*p2a+0.4*p2b+0.4*p2c
        if p2 == 1:
            outp.write('The script %s is structured properly.\n\n' % repr(file))
        else:
            outp.write('\n')
    else:
        p2 = 0
    
    total = round(0.5*p1+0.5*p2,3)
    return total


if __name__ == '__main__':
    print(grade())