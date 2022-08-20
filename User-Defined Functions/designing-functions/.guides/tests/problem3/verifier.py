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
        return (msg,None)


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


def verify_result(file,step=0,outp=sys.stdout):
    """
    Verify that the result variable is created properly.
    
    The step parameter indicates whether we are trying to trim or not.
    
    Parameter name: The file name
    Precondition: name is a string of a file in the given workspace
    
    Parameter step: The current verfication/grading step
    Precondition: grade is 0 or 1
    
    Parameter outp: The output stream
    Precondition: outp is a stream writer
    """
    env = import_module(file)
    if type(env) == str:
        outp.write(env)
        return FAIL_CRASHES
    elif not hasattr(env.module,'second_in_list'):
        outp.write("File %s is missing the header for 'second_in_list'.\n" % repr(file))
        return FAIL_INCORRECT
    
    func = env.module.second_in_list
    if func('') != 'banana':
        outp.write("The function is not returning 'banana', as directed.\n")
        return FAIL_INCORRECT
    
    count = 3 if step else 2
    if len(func.__code__.co_varnames) > count:
        outp.write("The function 'second_in_list' has more than %d local variable%s.\n" % (count-1,'s' if step else ''))
        return FAIL_INCORRECT
        
    
    # Now some code checking
    text = read_file(file).split('\n')
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
            return FAIL_INCORRECT
    
    if len(functions) != 1:
        outp.write("The module 'func' has functions other than 'second_in_list'.\n")
        return FAIL_INCORRECT
    
    body = functions['second_in_list'].body
    
    # Check the return statement
    variable = None
    for item in body:
        if type(item) == ast.Return:
            if type(item.value) != ast.Name:
                outp.write("The function 'second_in_list' is returning a complex expression instead of a single variable.\n")
                outp.write(text[item.value.lineno-1]+'\n')
                outp.write(' '*item.value.col_offset+'^\n')
                return FAIL_INCORRECT
            else:
                variable = item.value.id
    
    # Find the missing variables
    stubass = None
    for item in body:
        if type(item) == ast.Assign and type(item.value) == ast.Str:
            if len(item.targets) != 1 or type(item.targets[0]) != ast.Name:
                outp.write('Unexpected Python command at line %d:\n' % item.lineno)
                outp.write(text[item.lineno-1]+'\n')
                outp.write(' '*item.col_offset+'^\n')
                return FAIL_INCORRECT
            else:
                stubass = item
    
    if stubass is None:
        outp.write("Could not locate the stub assignment for the %s value'.\n" % ('pre-trimmed' if step else 'result'))
        return FAIL_INCORRECT
    
    code = text[functions['second_in_list'].lineno:stubass.lineno-1]+text[stubass.lineno:]
    code = ['import introcs','def second_in_list(s,'+stubass.targets[0].id+'):']+code
    original = stubass.value.s
    
    try:
        context = {}
        exec('\n'.join(code),context)
        second_in_list = context['second_in_list']
    except:
        outp.write("The function 'second_in_list' is not formatted correctly.\n")
        outp.write(traceback.format_exc(0)+'\n')
        return FAIL_INCORRECT
    
    if step:
        tests = [('   apple,   fig   ,  banana  ', '   fig   '), ('  do  ,  re  ,  me  ,  fa  ', '  re  ')]
        for pair in tests:
            if second_in_list(*pair) != pair[1].strip():
                outp.write("Your code fails if we replace the assignment for %s with %s.\n" % (repr(original), repr(pair[1])))
                return FAIL_INCORRECT
    else:
        tests = [('apple, fig,  banana  ', 'fig'), ('do, re, me, fa', 're')]
        for pair in tests:
            if second_in_list(*pair) != pair[1]:
                outp.write("Your code fails if we replace the assignment for %s with %s.\n" % (repr(original), repr(pair[1])))
                return FAIL_INCORRECT
    
    return TEST_SUCCESS


def verify_slice(file,outp=sys.stdout):
    """
    Verify that the item is properly sliced out of the string.
    
    Parameter name: The file name
    Precondition: name is a string of a file in the given workspace
    
    Parameter outp: The output stream
    Precondition: outp is a stream writer
    """
    env = import_module(file)
    if type(env) == str:
        outp.write(env)
        return FAIL_CRASHES
    elif not hasattr(env.module,'second_in_list'):
        outp.write("File %s is missing the header for 'second_in_list'.\n" % repr(file))
        return FAIL_INCORRECT
    
    func = env.module.second_in_list
    tests = [('apple, banana, orange', 'banana'), ('Billy, Andrew, Wendy', 'Andrew'), ('apple,   fig , orange', 'fig')]
    for pair in tests:
        try:
            if func(pair[0]) != pair[1]:
                outp.write("The function is not correct on %s, which should work at this step.\n" % repr(pair[0]))
                return FAIL_INCORRECT
        except:
            outp.write("The function crashed on input %s.\n" % repr(pair[0]))
            return FAIL_INCORRECT
    
    # Now some code checking
    text = read_file(file).split('\n')
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
            return FAIL_INCORRECT
    
    if len(functions) != 1:
        outp.write("The module 'func' has functions other than 'second_in_list'.\n")
        return FAIL_INCORRECT
    
    body = functions['second_in_list'].body
    
    # Find the missing variables
    stubass = []
    for item in body:
        if type(item) == ast.Assign and type(item.value) == ast.Str:
            outp.write('You still have an old stub assignment at line %d:\n' % item.lineno)
            outp.write(text[item.lineno-1]+'\n')
            outp.write(' '*item.col_offset+'^\n')
            return FAIL_INCORRECT
        elif type(item) == ast.Assign and type(item.value) == ast.Num:
            if len(item.targets) != 1 or type(item.targets[0]) != ast.Name:
                outp.write('Unexpected Python command at line %d:\n' % item.lineno)
                outp.write(text[item.lineno-1]+'\n')
                outp.write(' '*item.col_offset+'^\n')
                return FAIL_INCORRECT
            else:
                stubass.append(item)
    
    if stubass == []:
        outp.write("Could not locate the stub assignments for the slice locations.\n")
        return FAIL_INCORRECT
    elif len(stubass) == 1:
        outp.write("Could only locate one of the stub assignments for the slice locations.\n")
        return FAIL_INCORRECT
    elif len(stubass) > 2:
        outp.write("There are more than two stub assignments for the slice locations.\n")
        return FAIL_INCORRECT
    
    if stubass[0].value.n > stubass[1].value.n:
        tmp = stubass[0]
        stubass[0] = stubass[1]
        stubass[1] = tmp
    
    code = text[functions['second_in_list'].lineno:stubass[0].lineno-1]+text[stubass[0].lineno:stubass[1].lineno-1]+text[stubass[1].lineno:]
    code = ['import introcs','def second_in_list(s,'+stubass[0].targets[0].id+','+stubass[1].targets[0].id+'):']+code
    first = stubass[0].value.n
    secnd = stubass[1].value.n
    
    try:
        context = {}
        exec('\n'.join(code),context)
        second_in_list = context['second_in_list']
    except:
        outp.write("The function 'second_in_list' is not formatted correctly.\n")
        outp.write(traceback.format_exc(0)+'\n')
        return FAIL_INCORRECT
    
    tests = [('apple, fig, banana',5,10,'fig'), ('  do  ,  re  ,  me  ,  fa  ', 7,13,'re'),('z,y,x,w',1,3,'y')]
    for pair in tests:
        if second_in_list(*pair[:-1]) != pair[-1]:
            if pair[1] == first:
                msg = '%s with %s' % (repr(secnd),repr(pair[2]))
            elif pair[2] == secnd:
                msg = '%s with %s' % (repr(first),repr(pair[1]))
            else:
                msg = '%s with %s, and %s with %s' % (repr(first),repr(pair[1]),repr(secnd),repr(pair[2]))
            
            outp.write("Function 'second_in_list' fails on input %s if we replace %s.\n" % (repr(pair[0]), msg))
            outp.write("Remember, the two stubbed variables should be at the comma locations.\n")
            return FAIL_INCORRECT
    
    return TEST_SUCCESS


def verify_tail(file,outp=sys.stdout):
    """
    Verify that the tail is properly located.
    
    Parameter name: The file name
    Precondition: name is a string of a file in the given workspace
    
    Parameter outp: The output stream
    Precondition: outp is a stream writer
    """
    env = import_module(file)
    if type(env) == str:
        outp.write(env)
        return FAIL_CRASHES
    elif not hasattr(env.module,'second_in_list'):
        outp.write("File %s is missing the header for 'second_in_list'.\n" % repr(file))
        return FAIL_INCORRECT
    
    func = env.module.second_in_list
    tests = [('apple, banana, orange', 'banana'), ('Billy, Andrew, Wendy', 'Andrew'), ('apple,   fig , orange', 'fig'), ('apple, fig, orange', 'fig')]
    for pair in tests:
        try:
            if func(pair[0]) != pair[1]:
                outp.write("The function is not correct on %s, which should work at this step.\n" % repr(pair[0]))
                return FAIL_INCORRECT
        except:
            outp.write("The function crashed on input %s.\n" % repr(pair[0]))
            return FAIL_INCORRECT
    
    # Now some code checking
    text = read_file(file).split('\n')
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
            return FAIL_INCORRECT
    
    if len(functions) != 1:
        outp.write("The module 'func' has functions other than 'second_in_list'.\n")
        return FAIL_INCORRECT
    
    body = functions['second_in_list'].body
    
    # Find the missing variables
    stubass = []
    for item in body:
        if type(item) == ast.Assign and type(item.value) == ast.Str:
            outp.write('You still have an old stub assignment at line %d:\n' % item.lineno)
            outp.write(text[item.lineno-1]+'\n')
            outp.write(' '*item.col_offset+'^\n')
            return FAIL_INCORRECT
        elif type(item) == ast.Assign and type(item.value) == ast.Num:
            if len(item.targets) != 1 or type(item.targets[0]) != ast.Name:
                outp.write('Unexpected Python command at line %d:\n' % item.lineno)
                outp.write(text[item.lineno-1]+'\n')
                outp.write(' '*item.col_offset+'^\n')
                return FAIL_INCORRECT
            else:
                stubass.append(item)
    
    if stubass == []:
        outp.write("Could not locate the stub assignments for the slice locations'.\n")
        return FAIL_INCORRECT
    elif len(stubass) > 1:
        outp.write("There is more than one remaining stub assignments for the slice locations'.\n")
        return FAIL_INCORRECT
    
    code = text[functions['second_in_list'].lineno:stubass[0].lineno-1]+text[stubass[0].lineno:]
    code = ['import introcs','def second_in_list(s,'+stubass[0].targets[0].id+'):']+code
    first = stubass[0].value.n
    
    try:
        context = {}
        exec('\n'.join(code),context)
        second_in_list = context['second_in_list']
    except:
        outp.write("The function 'second_in_list' is not formatted correctly.\n")
        outp.write(traceback.format_exc(0)+'\n')
        return FAIL_INCORRECT
    
    tests = [('  do  ,  re  ,  me  ,  fa  ', 7,'re'),('z,y,x,w',1,'y')]
    for pair in tests:
        if second_in_list(*pair[:-1]) != pair[-1]:
            msg = '%s with %s' % (repr(first),repr(pair[1]))
            outp.write("Function 'second_in_list' fails on input %s if we replace %s.\n" % (repr(pair[0]), msg))
            outp.write("Remember, the stubbed variable should be at the first comma location.\n")
            return FAIL_INCORRECT
    
    return TEST_SUCCESS


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
        try:
            if func(pair[0]) != pair[1]:
                if not step:
                    outp.write("The function is not correct on %s, which should work at this step.\n" % repr(pair[0]))
                else:
                    outp.write("The call second_in_list(%s) returns %s, not %s.\n" % (repr(pair[0]), repr(func(pair[0])), repr(pair[1])))
                score -= 0.2
                if not step:
                    return (FAIL_INCORRECT,max(0,score))
        except:
            import traceback
            outp.write("The function 'second_in_list' crashed on valid input s=%s.\n" % repr(pair[0]))
            outp.write(traceback.format_exc(0))
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
    
    total = round(0.05*p1+0.95*p2,3)
    return total


def grade(outp=sys.stdout):
    """
    Invokes this subgrader (returning a percentage)
    """
    return grade_file('func.py',outp)


if __name__ == '__main__':
    print(grade())