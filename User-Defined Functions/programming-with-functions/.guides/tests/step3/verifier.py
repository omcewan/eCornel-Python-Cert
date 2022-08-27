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
    
    A matching pair pair of parentheses is an open parens '(' followed by a closing
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
    Parameter s: s is a string with a matching pair of parens '()'.
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


def match(s):
    """
    Correct function for comparison
    """
    first = s.find('(')
    secnd = s.find(')',first)
    return first != -1 and secnd != -1


def find(s):
    """
    Correct function for comparison
    """
    first = s.find('(')
    secnd = s.find(')',first)
    return s[first+1:secnd]


pass
#mark -
#mark Subgraders
def grade_first_in_parens(file,step=0,outp=sys.stdout):
    """
    Returns the test result and score for the implementation of first_in_parens
    
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
    env = import_module(file,0)
    if type(env) == str:
        outp.write(env)
        return (FAIL_CRASHES,0)
    
    # Step 1
    score = 1
    if not hasattr(env.module,'introcs'):
        outp.write("File %s does not imported 'introcs' as instructed.\n" % repr(file))
        return (FAIL_INCORRECT,0)
    elif not hasattr(env.module,'first_in_parens'):
        outp.write("File %s is missing the header for 'first_in_parens'.\n" % repr(file))
        return (FAIL_INCORRECT, 0)
    
    env.reset()
    func1 = env.module.first_in_parens
    func2 = find
    tests = [('A (B) C','B'), ('A (B) C (','B'), ('A (B) C )','B'), ('A (B) (C) D','B'),
             ('A (B (C) D) E','B (C'), ('A ) B (C) D','C'),('A () D',''),('(A D)','A D')]
    for pair in tests:
        try:
            if func1(pair[0]) != func2(pair[0]):
                outp.write("The call first_in_parens(%s) returned %s instead of %s.\n" % (repr(pair[0]),repr(func1(pair[0])),repr(func2(pair[0]))))
                score -= 0.1
                if not step:
                    return (FAIL_INCORRECT,max(0,score))
        except:
            import traceback
            outp.write("The call first_in_parens(%s) crashed.\n" % repr(pair[0]))
            outp.write(traceback.format_exc(0)+'\n')
            score -= 0.1
            if not step:
                return (FAIL_INCORRECT,max(0,score))
    
    # Make sure the student did not cheat
    text = read_file(file).split('\n')
    code = parse_file(file)
    if type(code) == str:
        outp.write(code)
        return (FAIL_CRASHES,max(0,score))
    elif type(code) != ast.Module:
        outp.write("File %s appears to be corrupted somehow.\n" % repr(file))
        return (FAIL_INCORRECT,max(0,score))
    
    func = None
    for item in code.body:
        if type(item) == ast.FunctionDef and item.name == 'first_in_parens':
            func = item
    
    if not func:
        outp.write("File %s appears to be corrupted somehow.\n" % repr(file))
        return (FAIL_INCORRECT,max(0,score))
    else:
        badline = None
        for item in ast.walk(func):
            if type(item) == ast.If:
                badline = item
        if badline:
            outp.write("The function 'first_in_parens' uses an if-statement at line %d:\n" % badline.lineno)
            outp.write(text[badline.lineno-1]+'\n')
            outp.write(' '*badline.col_offset+'^\n')
            score -= 0.15
            if not step:
                return (FAIL_INCORRECT, max(0,score))
    
    return (TEST_SUCCESS, max(0,score))


def grade_matching_parens(file,step=0,outp=sys.stdout):
    """
    Returns the test result and score for the implementation of matching_parens
    
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
    env = import_module(file,0)
    if type(env) == str:
        outp.write(env)
        return (FAIL_CRASHES,0)
    
    # Step 1
    score = 1
    if not hasattr(env.module,'introcs'):
        outp.write("File %s does not imported 'introcs' as instructed.\n" % repr(file))
        return (FAIL_INCORRECT,0)
    elif not hasattr(env.module,'matching_parens'):
        outp.write("File %s is missing the header for 'matching_parens'.\n" % repr(file))
        return (FAIL_INCORRECT, 0)
    
    env.reset()
    func1 = env.module.matching_parens
    func2 = match
    tests = [('',False), ('A',False), ('A )B( C',False), ('A B) C',False), ('A (B C',False),
             ('A (B) C',True), ('A (B) C (',True), ('A (B) C )',True), ('A (B) (C) D',True),
             ('A (B (C) D) E',True), ('A ) B (C) D',True)]
    for pair in tests:
        try:
            if func1(pair[0]) != func2(pair[0]):
                outp.write("The call matching_parens(%s) returned %s instead of %s.\n" % (repr(pair[0]),repr(func1(pair[0])),repr(func2(pair[0]))))
                score -= 0.1
                if not step:
                    return (FAIL_INCORRECT,max(0,score))
        except:
            import traceback
            outp.write("The call matching_parens(%s) crashed.\n" % repr(pair[0]))
            outp.write(traceback.format_exc(0)+'\n')
            score -= 0.1
            if not step:
                return (FAIL_INCORRECT,max(0,score))
    
    # Make sure the student did not cheat
    text = read_file(file).split('\n')
    code = parse_file(file)
    if type(code) == str:
        outp.write(code)
        return (FAIL_CRASHES,max(0,score))
    elif type(code) != ast.Module:
        outp.write("File %s appears to be corrupted somehow.\n" % repr(file))
        return (FAIL_INCORRECT,max(0,score))
    
    func = None
    for item in code.body:
        if type(item) == ast.FunctionDef and item.name == 'matching_parens':
            func = item
    
    if not func:
        outp.write("File %s appears to be corrupted somehow.\n" % repr(file))
        return (FAIL_INCORRECT,max(0,score))
    else:
        badline = None
        for item in ast.walk(func):
            if type(item) == ast.If:
                badline = item
        if badline:
            outp.write("The function 'matching_parens' uses an if-statement at line %d:\n" % badline.lineno)
            outp.write(text[badline.lineno-1]+'\n')
            outp.write(' '*badline.col_offset+'^\n')
            score -= 0.15
            if not step:
                return (FAIL_INCORRECT, max(0,score))
    
    return (TEST_SUCCESS, max(0,score))



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
    outp.write("Function 'matching_parens' comments:\n")
    status, p1 = grade_matching_parens(file,1,outp)
    if p1 == 1:
        outp.write("The implementation of 'matching_parens' looks good.\n\n")
    else:
        outp.write('\n')
    
    if not status:
        outp.write("Function 'first_in_parens' comments:\n")
        status, p2 = grade_first_in_parens(file,1,outp)
        if p2 == 1:
            outp.write("The implementation of 'first_in_parens' looks good.\n\n")
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
    return grade_file('funcs.py',outp)


if __name__ == '__main__':
    print(grade())