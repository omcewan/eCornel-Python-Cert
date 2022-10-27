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
import math
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


WORKSPACE = [os.path.expanduser('~'),'workspace','exercise4']
#WORKSPACE = []


#mark -
#mark Test Capture
class TestPlan(object):

    @property
    def tested(self):
        """
        The captured print statements of this environment.

        Each call to `print` is a separate entry to this list.  Special
        endlines (or files) are ignored.

        **Invariant**: Value is a list of strings.
        """
        return self._tests

    @property
    def asserted(self):
        """
        The captured input statements of this environment.

        Each call to `input` adds a new element to the list.  Only the
        prompts are added to this list, not the user response (which
        are specified in the initializer).

        **Invariant**: Value is a list of strings or None.
        """
        return self._asserts
    
    def __init__(self,env):
        self._environment = env
        self._tests   = {}
        self._asserts = {}
    
    def reset(self):
        self._tests   = {}
        self._asserts = {}
    
    def assert_equals(self,expected,received,message=None):
        """
        Wrapper for introcs.assert_equals
        """
        if not 'assert_equals' in self._asserts:
            self._asserts['assert_equals'] = []
        self._asserts['assert_equals'].append((expected,received))
    
    def assert_not_equals(self,expected,received,message=None):
        """
        Wrapper for introcs.assert_not_equals
        """
        if not 'assert_not_equals' in self._asserts:
            self._asserts['assert_not_equals'] = []
        self._asserts['assert_not_equals'].append((expected,received))
    
    def assert_true(self,received,message=None):
        """
        Wrapper for introcs.assert_true
        """
        if not 'assert_true' in self._asserts:
            self._asserts['assert_true'] = []
        self._asserts['assert_true'].append(received)
    
    def assert_false(self,received,message=None):
        """
        Wrapper for introcs.assert_false
        """
        if not 'assert_false' in self._asserts:
            self._asserts['assert_false'] = []
        self._asserts['assert_false'].append(received)
    
    def assert_floats_equal(self,expected, received,message=None):
        """
        Wrapper for introcs.assert_floats_equal
        """
        if not 'assert_floats_equal' in self._asserts:
            self._asserts['assert_floats_equal'] = []
        self._asserts['assert_floats_equal'].append((expected,received))
    
    def assert_floats_not_equal(self,expected, received,message=None):
        """
        Wrapper for introcs.assert_floats_not_equal
        """
        if not 'assert_floats_not_equal' in self._asserts:
            self._asserts['assert_floats_not_equal'] = []
        self._asserts['assert_floats_not_equal'].append((expected,received))
    
    def circ_area1(self,**arg):
        """
        Incorrect version for first pass
        """
        if not 'avg' in self._tests:
            self._tests['circ_area'] = []
        self._tests['circ_area'].append(arg)
        return None
    
    def circ_area2(self,**arg):
        """
        Correct version
        """
        self._environment.print('___test___')
        if not 'circ_area' in self._tests:
            self._tests['circ_area'] = []
        self._tests['circ_area'].append(arg)
        return self.circ_area3(**arg)
    
    def circ_area3(self,**arg):
        """
        Correct version, no logging
        """
        radius = arg['radius'] if 'radius' in arg else arg['diameter']/2
        return math.pi*radius*radius


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


def import_module(name,step=0,test=True):
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
        if test:
            testplan = TestPlan(environment)
        
            intro = types.ModuleType('introcs')
            for func in dir(introcs):
                if func[0] != '_':
                    if 'assert' in func and hasattr(testplan,func):
                        setattr(intro,func,getattr(testplan,func))
                    else:
                        setattr(intro,func,getattr(introcs,func))
            environment.capture('introcs',intro)
        
            if step < 2:
                func = types.ModuleType('func')
                func.circ_area = testplan.circ_area2
                environment.capture('func',func)
            else:
                try:
                    func = Environment('func',WORKSPACE)
                    func.execute()
                    environment.capture('func',func.module)
                except:
                    pass
        else:
            testplan = None
        
        if not environment.execute():
            return ('\n'.join(environment.printed)+'\n',None)
        return (environment, testplan)
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
            outp.write("The second-to-last line in the docstring for %s does not start with 'Author:'\n" % repr(file))
            score -= 0.5
        if test == NAME_INCOMPLETE:
            outp.write("There is no name after 'Author:' in the docstring for %s.\n" % repr(file))
            score -= 0.4
        if not step:
            return (FAIL_BAD_STYLE,max(0,score))
    test = check_date(docs)
    if test:
        if test == DATE_MISSING:
            outp.write("The last line in the docstring for %s does not start with 'Date:'\n" % repr(file))
            score -= 0.5
        if test == DATE_INCOMPLETE:
            outp.write("The date after 'Date:' in the docstring for %s is invalid .\n"  % repr(file))
            score -= 0.4
        if not step:
            return (FAIL_BAD_STYLE, max(0,score))
    
    return (TEST_SUCCESS, max(0,score))


def grade_structure(file,step=0,outp=sys.stdout):
    """
    Returns the test result and score for the header of avg
    
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
    # Verify the structure is correct
    score = 1
    code = parse_file(file)
    function = 'circ_area'
    
    if type(code) == str:
        outp.write('There was a problem reading file %s.\n' % repr(file))
        outp.write(code+'\n')
        return (FAIL_NO_FILE, 0)
    
    # Find the function body
    body = None
    for item in code.body:
        if type(item) == ast.FunctionDef and item.name == function:
            body = item
    
    if body is None:
        outp.write("File %s is missing the definition for %s.\n" % (repr(file),repr(function)))
        return (FAIL_INCORRECT, 0)
    
    if body.args.kwarg is None:
        outp.write("The parameter for %s does not use keyword expansion, as directed\n." % repr(function))
        if not body.args.vararg is None and body.args.vararg.arg == 'kwd':
            outp.write("The function %s uses 'kwd' with tuple expansion, not keyword expansion.\n" % repr(function))
            score -= 0.5
            if not step:
                return (FAIL_INCORRECT,max(0,score))
        else:
            return (FAIL_INCORRECT,max(0,score))

    if body.args.args != []:
        if len(body.args.args) == 1 and body.args.args[0].arg == 'kwd':
            outp.write("The function %s does not use keyword expansion for 'kwd', as directed\n." % repr(function))
            score -= 0.5
            if not step:
                return (FAIL_INCORRECT,max(0,score))
        else:
            outp.write("The function %s contains positional parameters not mentioned in the specification.\n" % repr(function))
            score -= 0.2
            if not step:
                return (FAIL_INCORRECT,max(0,score))
    
    if body.args.kwonlyargs != []:
        outp.write("The function %s contains keyword parameters not mentioned in the specification.\n" % repr(function))
        score -= 0.2
        if not step:
            return (FAIL_INCORRECT,max(0,score))
    
    return (TEST_SUCCESS,max(0,score))


def grade_func(file,step=0,outp=sys.stdout):
    """
    Returns the test result and score for the implementation of isnetid
    
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
    env, tests = import_module(file,0)
    function = 'circ_area'
    
    if type(env) == str:
        outp.write(env)
        return (FAIL_CRASHES, 0)
    elif not hasattr(env.module,function):
        outp.write("File %s is missing the header for %s.\n" % (repr(file),repr(function)))
        return (FAIL_INCORRECT, 0)
    
    testcase = [({'radius':3},28.27433),({'radius':2},12.56637),
                ({'diameter':6},28.27433),({'diameter':4},12.56637),
                ({'radius':3,'foo':20,'bar':10},28.27433),
                ({'diameter':4,'foo':20,'bar':10},12.56637)]
    
    func = getattr(env.module,function)
    printed = False
    for data in testcase:
        arg = data[0]
        expected = data[1]
        try:
            env.reset()
            received = func(**arg)
            if type(received) != float or not introcs.isclose(received, expected):
                outp.write("The call %s(**%s) returns %s, not %s.\n" % (function, repr(arg), repr(received), repr(expected)))
                score -= 1/len(testcase)
                if not step:
                    return (FAIL_INCORRECT,max(0,score))
            if len(env.printed) != 0:
                printed = True
        except:
            outp.write("The call %s(**%s) crashed.\n" % (function, repr(arg)))
            outp.write(traceback.format_exc(0)+'\n')
            score -= 1/len(testcase)
            if not step:
                return (FAIL_INCORRECT,max(0,score))
    
    if printed:
        outp.write("You must remove all debugging print statements from %s.\n" % repr(function))
        score -= 0.1
        if not step:
            return (FAIL_BAD_STYLE,max(0,score))
    
    badcases = [{'foo':20,'bar':10},{'radius':3,'diameter':2},{'radius':3,'diameter':6},{}]
    for arg in badcases:
        try:
            env.reset()
            received = func(**arg)
            outp.write("The call %s(**%s) did not crash as expected.\n" % (function, repr(arg)))
            score -= 0.2/len(testcase)
            if not step:
                return (FAIL_INCORRECT,max(0,score))
        except AssertionError:
            pass
        except Exception as e:
            outp.write("The call %s(**%s) crashed with %s, not an AssertionError.\n" % (function, repr(arg), e.__class__.__name__))
            score -= 0.2/len(testcase)
            if not step:
                return (FAIL_INCORRECT,max(0,score))
    
    return (TEST_SUCCESS,max(0,score))


def grade_testcases(file,step=0,outp=sys.stdout):
    """
    Returns the test result and score for the test cases
    
    The step parameter is the phase in the grading pass.  Step 0 only looks for one
    test cases.  Step 1 looks for proper test coverage.  Steps 0-1 will stop at the 
    first error found.  Step 2 is the final grading pass and will continue through and 
    try to find all errors.
    
    Parameter name: The file name
    Precondition: name is a string of a file in the given workspace
    
    Parameter step: The current verfication/grading step
    Precondition: grade is 0 or 1
    
    Parameter outp: The output stream
    Precondition: outp is a stream writer
    """
    score = 1
    env, tests = import_module(file,0)
    if type(env) == str:
        outp.write(env)
        return (FAIL_CRASHES,0)
    
    function = 'circ_area'
    env.reset()
    tests.reset()
    try:
        tester = getattr(env.module,'test_'+function)
        tester()
    except:
        outp.write("The test procedure 'test_%s' crashed when called:\n" % function)
        outp.write(traceback.format_exc(0)+'\n')
        return (FAIL_INCORRECT,0)
    
    found1 = False
    for item in  tests.tested[function]:
        if len(item) > 1 and ('radius' in item or 'diameter' in item) and not ('radius' in item and 'diameter' in item):
            found1 = True
    
    if not found1:
        outp.write("You have not added a (valid) test case with additional keyword arguments.\n")
        score -= 0.5
        if not step:
            return (FAIL_INCORRECT,max(0,score))
    
    # Verify the structure is correct
    code = parse_file(file)
    if type(code) == str:
        outp.write('There was a problem reading file %s.\n' % repr(file))
        outp.write(code+'\n')
        return (FAIL_NO_FILE, 0)
    
    # Find the function body
    body = None
    for item in code.body:
        if type(item) == ast.FunctionDef and item.name == 'test_'+function:
            body = item
    
    if body is None:
        outp.write("File %s is missing the test procedure 'test_%s'.\n" % (repr(file),str(function)))
        return (FAIL_INCORRECT, 0)
    
    found1 = False
    found2 = False
    for item in ast.walk(body):
        if type(item) == ast.Call and type(item.func) == ast.Name and item.func.id == function:
            if len(item.args) == 0 and len(item.keywords) == 1 and item.keywords[0].arg is None:
                found1 = True
            elif len(item.args) == 0:
                for kw in item.keywords:
                    if not kw.arg in [None, 'radius', 'diameter']:
                        found2 = True
        elif type(item) == ast.Call and type(item.func) == ast.Attribute and item.func.attr == function:
            if len(item.args) == 0 and len(item.keywords) == 1 and item.keywords[0].arg is None:
                found1 = True
            elif len(item.args) == 0:
                for kw in item.keywords:
                    if not kw.arg in [None, 'radius', 'diameter']:
                        found2 = True

    if not found1 or found2:
        outp.write("The additional test case does not call %s using a ** expression.\n" % repr(function))
        score -= 0.5
        if not step:
            return (FAIL_INCORRECT,max(0,score))
    
    for key in tests.asserted:
        if not key in ['assert_floats_equal','assert_true'] and len(tests.asserted[key]) > 0:
            outp.write("You should only use 'assert_float_equals' or 'assert_true' for your test cases, not %s.\n" % repr(key))
            if not step:
                score -= 0.2
                return (FAIL_INCORRECT, max(0,score))
        elif key == 'assert_floats_equal':
            for pos in range(len(tests.asserted[key])):
                pair = tests.asserted[key][pos]
                if type(pair[0]) != float or round(pair[0],4) != round(pair[1],4):
                    outp.write("The expected value %s for call number %d to %s is incorrect.\n" %(repr(pair[0]),repr(pos),repr(key)))
                    if not step:
                        score -= 0.2
                        return (FAIL_INCORRECT, max(0,score))
        elif key == 'assert_true':
            for pos in range(len(tests.asserted[key])):
                value = tests.asserted[key][pos]
                if type(value) != bool:
                    outp.write("The call %s should not be used when the function returns %s.\n" %(repr(key),repr(value)))
                    if not step:
                        score -= 0.2
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



def grade(outp=sys.stdout):
    """
    Invokes this subgrader (returning a percentage)
    
    Parameter outp: The output stream
    Precondition: outp is a stream writer
    """
    file1 = 'func.py'
    file2 = 'test.py'
    
    outp.write('Docstring comments:\n')
    status, p1a = grade_docstring(file1,1,outp)
    if not status:
       status, p1b = grade_docstring(file2,1,outp)
    else:
        p1b = 0
    p1 = 0.5*p1a+0.5*p1b
    if p1 == 1:
        outp.write('The docstrings for both files look good.\n\n')
    else:
        outp.write('\n')
    
    func = 'circ_area'
    if not status:
        outp.write("Comments for %s:\n" % repr(func))
        status, p2a = grade_structure(file1,1,outp)
        if not status:
            status, p2b = grade_func(file1,1,outp)
        else:
            p2b = 0
        p2 = 0.25*p2a+0.75*p2b
        if p2 == 1:
            outp.write('The function looks good.\n\n')
        else:
            outp.write('\n')
    else:
        p2 = 0
    
    if not status:
        outp.write("Test case comments:\n")
        status, p3 = grade_testcases(file2,1,outp)
        if p3 == 1:
            outp.write('The test cases look good.\n\n')
        else:
            outp.write('\n')
    else:
        p3 = 0
    
    total = round(0.05*p1+0.55*p2+0.4*p3,3)
    return total

if __name__ == '__main__':
    print(grade())