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


WORKSPACE = [os.path.expanduser('~'),'workspace','exercise3']
#WORKSPACE = []


DOCSTRING = """
    Returns: The initials <first>. <last>. of the given name.
    
    We assume that n is just two names (first and last). Middle names are
    not supported.
    
    Example: initials('John Smith') returns 'J. S.'
    Example: initials('Walker White') returns 'W. W.'
    
    Parameter n: the person's name
    Precondition: n is in the form 'first-name last-name' with one space between names.
    There are no spaces in either <first-name> or <last-name>
    """

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
#mark Special Type
class Special(object):
    """
    Singleton object to test error messages
    """
    def __str__(self):
        """
        Returns the string representation of this object.
        """
        return 'STR_VALUE'
    
    def __repr__(self):
        """
        Returns the canonical representation of this object.
        """
        return 'REPR_VALUE'


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
    
    test = check_name(docs)
    if test:
        if test == NAME_MISSING:
            outp.write("The second-to-last line in the docstring does not start with 'Author:'\n")
            score -= 0.3
        if test == NAME_INCOMPLETE:
            outp.write("There is no name after 'Author:'\n")
            score -= 0.1
        if not step:
            return (FAIL_BAD_STYLE,max(0,score))
    test = check_date(docs)
    if test:
        if test == DATE_MISSING:
            outp.write("The last line in the docstring does not start with 'Date:'\n")
            score -= 0.2
        if test == DATE_INCOMPLETE:
            outp.write("The date after 'Date:' is invalid.\n")
            score -= 0.1
        if not step:
            return (FAIL_BAD_STYLE, max(0,score))
    
    return (TEST_SUCCESS, max(0,score))


def grade_func(file,step=0,outp=sys.stdout):
    """
    Returns the test result and score for the function implementation
    
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
    elif not hasattr(env.module,'second_in_list'):
        outp.write("File %s is missing the header for 'second_in_list'.\n" % repr(file))
        return (FAIL_INCORRECT, 0)
    
    func = env.module.second_in_list
    tests = [('apple, banana, orange', 'banana'), ('Billy, Andrew, Wendy', 'Andrew'), 
             ('apple,   fig , orange', 'fig'), ('apple, fig, orange', 'fig'),
             ('  do  ,  re  ,  me  ,  fa  ','re'), ('z,y,x,w','y'), ('abc,def,geh','def'),
             (',,','')]
    for pair in tests:
        if func(pair[0]) != pair[1]:
            if not step:
                outp.write("The function is not correct on %s, which should work at this step.\n" % repr(pair[0]))
            else:
                outp.write("The call second_in_list(%s) returns %s, not %s.\n" % (repr(pair[0]), repr(func(pair[0])), repr(pair[1])))
            score -= 0.2
            if not step:
                return (FAIL_INCORRECT,max(0,score))
    
    # Now some final code checking
    node = parse_file(file)
    
    functions = {}
    for item in node.body:
        if type(item) == ast.FunctionDef:
            functions[item.name] = item
        elif (type(item) == ast.Expr and type(item.value) == ast.Str) or (type(item) == ast.Import):
            pass
        else:
            outp.write('Unexpected Python command at line %d:\n' % item.lineno)
            outp.write(text[item.lineno-1]+'\n')
            outp.write(' '*item.col_offset+'^\n')
            score -= 0.2
            if not step:
                return (FAIL_INCORRECT,max(0,score))
    
    if len(functions) != 1:
        outp.write("The module 'func' has functions other than 'second_in_list'.\n")
        score -= 0.1
        if not step:
            return (FAIL_INCORRECT,max(0,score))
    
    body = functions['second_in_list'].body
    
    # Find the missing variables
    stubass = []
    for item in body:
        if type(item) == ast.Assign and type(item.value) in [ast.Str, ast.Num]:
            outp.write('You still have an old stub assignment at line %d:\n' % item.lineno)
            outp.write(text[item.lineno-1]+'\n')
            outp.write(' '*item.col_offset+'^\n')
            score -= 0.2
            if not step:
                return (FAIL_INCORRECT,max(0,score))
    
    return (TEST_SUCCESS,max(0,score))


def grade_asserts(file,step=0,outp=sys.stdout):
    """
    Returns the test result and score for the assert statements
    
    The step parameter is the phase in the grading pass.  Step 0 verifies that type
    (str) is enforced.  Step 1 verifies that structure (two commas) is enforced as 
    well.  Steps 0-1 will stop at the first error found.  Step 2 is a grading pass and
    will continue through and try to find all errors.
    
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
    elif not hasattr(env.module,'second_in_list'):
        outp.write("File %s is missing the header for 'second_in_list'.\n" % repr(file))
        return (FAIL_INCORRECT, 0)
    
    func = env.module.second_in_list
    tests = ['a,b,c','a,b,c,d']
    for item in tests:
        try:
            func(item)
        except:
            import traceback
            outp.write("The function 'second_in_list' no longer works on valid input s=%s.\n" % repr(item))
            outp.write(traceback.format_exc(0)+'\n')
            score -= 0.2
            if step < 2:
                return (FAIL_INCORRECT, max(0,score))
    
    tests = [12,35.0,True]
    for item in tests:
        try:
            func(item)
            outp.write("The function 'second_in_list' did not enforce the precondition for s=%s.\n" % repr(item))
            score -= 0.2
            if step < 2:
                return (FAIL_INCORRECT, max(0,score))
        except AssertionError:
            pass
        except:
            outp.write("The function 'second_in_list' did not enforce the precondition for s=%s.\n" % repr(item))
            score -= 0.2
            if step < 2:
                return (FAIL_INCORRECT, max(0,score))
    
    if step:
        tests = ['a','a,']
        for item in tests:
            try:
                func(item)
                outp.write("The function 'second_in_list' did not enforce the precondition for s=%s.\n" % repr(item))
                score -= 0.25
                if step < 2:
                    return (FAIL_INCORRECT, max(0,score))
            except AssertionError:
                pass
            except:
                outp.write("The function 'second_in_list' did not enforce the precondition for s=%s.\n" % repr(item))
                score -= 0.25
                if step < 2:
                    return (FAIL_INCORRECT, max(0,score))
    else:
        tests = ['a','a,']
        for item in tests:
            try:
                func(item)
            except AssertionError:
                outp.write('You should only have an assert for the type at this step.\n')
                return (FAIL_INCORRECT, max(0,score))
            except:
                pass
    
    return (TEST_SUCCESS,max(0,score))


def grade_messages(file,step=0,outp=sys.stdout):
    """
    Returns the test result and score for the error messages
    
    The step parameter is the phase in the grading pass.  Step 0 verifies the error
    message for the first assert. Step 1 verifies the error message for the second assert.
    Steps 0-1 will stop at the first error found.  Step 2 is a grading pass and
    will continue through and try to find all errors.
    
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
    elif not hasattr(env.module,'second_in_list'):
        outp.write("File %s is missing the header for 'second_in_list'.\n" % repr(file))
        return (FAIL_INCORRECT, 0)
    
    func = env.module.second_in_list
    tests = ['a,b,c','a,b,c,d']
    for item in tests:
        try:
            func(item)
        except:
            outp.write("The function 'second_in_list' no longer works on valid input s=%s.\n" % repr(item))
            score -= 0.2
            if step < 2:
                return (FAIL_INCORRECT, max(0,score))
    
    tests = [12,35.0,True,Special()]
    for item in tests:
        try:
            func(item)
            outp.write("The function 'second_in_list' did not enforce the precondition for s=%s.\n" % repr(item))
            score -= 0.2
            if step < 2:
                return (FAIL_INCORRECT, max(0,score))
        except AssertionError as e:
            if len(e.args) == 0:
                outp.write("The type assert 'second_in_list' has no error message.\n")
                score -= 0.2
                if step < 2:
                    return (FAIL_INCORRECT, max(0,score))
            else:
                message = e.args[0]
                correct = 'The value %s is not a string.' % repr(item)
                alternt = 'The value %s is not a string.' % str(item)
                if message != correct:
                    if message[:-1] == correct[:-1]:
                        outp.write("The error message for the type assert is missing a period.\n")
                    elif message == alternt:
                        outp.write("The error message uses str() and not repr() as directed.\n")
                    else:
                        outp.write("The error message for the type assert is incorrect for value %s.\n" % repr(item))
                    score -= 0.2
                    if step < 2:
                        return (FAIL_INCORRECT, max(0,score))
        except:
            outp.write("The function 'second_in_list' did not enforce the precondition for s=%s.\n" % repr(item))
            score -= 0.2
            if step < 2:
                return (FAIL_INCORRECT, max(0,score))
    
    tests = ['a','a,']
    for item in tests:
        try:
            func(item)
            func(item)
            outp.write("The function 'second_in_list' did not enforce the precondition for s=%s.\n" % repr(item))
            score -= 0.2
            if step < 2:
                return (FAIL_INCORRECT, max(0,score))
        except AssertionError as e:
            if not step:
                if len(e.args) > 0:
                    outp.write('You should only have an error message for the first assert at this step.\n')
                    score -= 0.1
                    return (FAIL_INCORRECT, max(0,score))
            else:
                if len(e.args) == 0:
                    outp.write("The comma assert 'second_in_list' has no error message.\n")
                    score -= 0.2
                    if step < 2:
                        return (FAIL_INCORRECT, max(0,score))
                else:
                    message = e.args[0]
                    correct = 'The string %s does not have enough commas.' % repr(item)
                    if message != correct:
                        if message[:-1] == correct[:-1]:
                            outp.write("The error message for the comma assert is missing a period.\n")
                        else:
                            outp.write("The error message for the comma assert is incorrect for value %s.\n" % repr(item))
                        score -= 0.2
                        if step < 2:
                            return (FAIL_INCORRECT, max(0,score))
        except:
            outp.write("The function 'second_in_list' did not enforce the precondition for s=%s.\n" % repr(item))
            score -= 0.25
            if step < 2:
                return (FAIL_INCORRECT, max(0,score))

    
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
        outp.write('Function comments:\n')
        status, p2 = grade_func(file,1,outp)
        if p2 == 1:
            outp.write('The function looks good.\n\n')
        else:
            outp.write('\n')
    else:
        p2 = 0
    
    if not status:
        outp.write('Error Message comments:\n')
        status, p3 = grade_messages(file,2,outp)
        if p3 == 1:
            outp.write('The error messages look good.\n\n')
        else:
            outp.write('\n')
    else:
        p3 = 0
    
    total = round(0.05*p1+0.1*p2+0.85*p3,3)
    return total


def grade(outp=sys.stdout):
    """
    Invokes this subgrader (returning a percentage)
    """
    return grade_file('func.py',outp)


if __name__ == '__main__':
    print(grade())