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
    
    def iso1(self,s):
        """
        Incorrect version for first pass
        """
        if not 'iso_8601' in self._tests:
            self._tests['iso_8601'] = []
        self._tests['iso_8601'].append(s)
        return None
    
    def iso2(self,s):
        """
        Correct version
        """
        self._environment.print('___test___')
        if not 'iso_8601' in self._tests:
            self._tests['iso_8601'] = []
        self._tests['iso_8601'].append(s)
        return self.iso3(s)
    
    def iso3(self,s):
        """
        Correct version, no logging
        """
        try:
            pos1 = introcs.index_str(s,':')
            pos2 = introcs.index_str(s,':',pos1+1)
            hour = int(s[:pos1])
            mins = int(s[pos1+1:pos2])
            secs = int(s[pos2+1:])
        
            # Check times in range
            correct = hour >= 0 and hour < 24 and mins >= 0 and mins < 60 and secs >= 0 and secs < 60
            # Check digits correct
            correct = correct and pos2 == pos1+3 and len(s) == pos2+3
            return correct
        except:
            return False



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
                if step:
                    func.iso_8601 = testplan.iso2
                else:
                    func.iso_8601 = testplan.iso1
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
#mark Test Case Checking
def encode_iso(input):
    """
    Returns: the hash encoding for input to iso_8601
    
    Parameter input: The input to pigify
    Precondition: s is a non-empty string with all lower case letters
    """
    """
    The test encoder for has_a_vowel
    """
    if type(input) != str:
        return -1
    elif len(input) == 0:
        return 14
    
    pos1 = input.find(':')
    pos2 = input.find(':',pos1+1)
    
    if pos2 != -1 and ':' in input[pos2+1:]:
        return 15
    
    if pos1 == -1:
        if input.isdigit():
            return 2
        else:
            return 1
    elif not input[:pos1].isdigit():
        return 8
    else:
        hours = int(input[:pos1])
        if hours < 0 or hours > 23:
            return 13
    
    if pos2 == -1:
        if input[pos1+1:].isdigit():
            return 3
        else:
            return 7
    elif not input[pos1+1:pos2].isdigit():
        return 7
    else:
        mins = int(input[pos1+1:pos2])
        if mins < 0 or mins > 59:
            return 12
    
    if not input[pos2+1:].isdigit():
        return 6
    else:
        secs = int(input[pos2+1:])
        if secs < 0 or secs > 59:
            return 11
    
    if mins < 10 and pos2 == pos1+2:
        return 10
    elif secs < 10 and len(input) == pos2+2:
        return 9
    
    return 5 if pos1 == 1 else 4


# The explanatory reasons for the tests
TEST_ISO = [
    "a test with unrecognizable hours, minutes, or seconds",
    "a test with hours, but not minutes or seconds",
    "a test with hours and minutes, but no seconds",
    "a test with a proper string and 2-digit hours",
    "a test with a proper string and 1-digit hours",
    "a test with non-integer seconds",
    "a test with non-integer minutes",
    "a test with non-integer hours",
    "a test with single-digit seconds and no padding 0",
    "a test with single-digit minutes and no padding 0",
    "a test with seconds out of range",
    "a test with minutes out of range",
    "a test with hours out of range",
    "a test with an empty string",
    "a test with more than 2 colons"
]


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
            outp.write('The module docstring in %s is not properly closed.\n'  % repr(file))
            return (FAIL_CRASHES,0.1)
        if docs == DOCSTRING_NOT_FIRST:
            outp.write('The module docstring in %s is not the first non-blank line.\n'  % repr(file))
            score -= 0.3
        if not step:
            return (FAIL_BAD_STYLE,max(0,score))
    docs = get_docstring(code,False)
    
    test = check_name(docs)
    if test:
        if test == NAME_MISSING:
            outp.write("The second-to-last line in the docstring for %s does not start with 'Author:'\n"  % repr(file))
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
            outp.write("The date after 'Date:' in the docstring for %s is invalid .\n" % repr(file))
            score -= 0.4
        if not step:
            return (FAIL_BAD_STYLE, max(0,score))
    
    return (TEST_SUCCESS, max(0,score))


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
    env, tests = import_module(file,0)
    if type(env) == str:
        outp.write(env)
        return (FAIL_CRASHES,0)
    
    # So we can adapt this template to others
    function = 'iso_8601'
    correct  = tests.iso3
    encoder  = encode_iso
    REASONS  = TEST_ISO
    wtests = 10 if step else 2
    
    # Step 1
    score = 1
    if not hasattr(env.module,'introcs') or not hasattr(env.module,'func'):
        outp.write("You have modified the import statements in %s, violating the instructions.\n" % repr(file))
        return (FAIL_INCORRECT,0)
    elif not hasattr(env.module,'test_'+function):
        outp.write("File %s is missing the test procedure 'test_%s'.\n" % (repr(file),function))
        return (FAIL_INCORRECT,0)
    
    env.reset()
    tests.reset()
    try:
        tester = getattr(env.module,'test_'+function)
        tester()
    except:
        import traceback
        outp.write("The test procedure 'test_%s' crashed when called:\n" % function)
        outp.write(traceback.format_exc(0)+'\n')
        return (FAIL_INCORRECT,0)
    
    if not function in tests.tested:
        outp.write("You have not called the function %s properly.\n" % repr(function))
        return (FAIL_INCORRECT,0)
    elif not 'assert_equals' in tests.asserted or len(tests.asserted['assert_equals']) != len(tests.tested[function]):
        outp.write("You were supposed to call 'assert_equals' for each test case.\n")
        score -= 0.1
        if step < 2:
            return (FAIL_INCORRECT, max(0,score))
    
    badin = None
    for pos in range(len(tests.asserted['assert_equals'])):
        if  pos < len(tests.tested[function]):
            pair  = tests.asserted['assert_equals'][pos]
            input = tests.tested[function][pos]
            if pair[0] != correct(input) and encoder(input) >= 0:
                badin = input
    
    if badin:
        outp.write("In 'assert_equals', the expected value goes first [see %s].\n" % repr(badin))
        score -= 0.1
        if step < 2:
            return (FAIL_BAD_STYLE,0)
    
    env, tests = import_module(file,1)
    if type(env) == str:
        outp.write(env)
        return (FAIL_CRASHES,0)
    
    env.reset()
    tests.reset()
    try:
        tester = getattr(env.module,'test_'+function)
        tester()
    except:
        import traceback
        outp.write("The test procedure 'test_%s' crashed when called:\n" % function)
        outp.write(traceback.format_exc(0)+'\n')
        return (FAIL_INCORRECT,0)
    
    if not 'assert_equals' in tests.asserted or len(tests.asserted['assert_equals']) != len(tests.tested[function]):
        outp.write("You were supposed to call 'assert_equals' for each test case [second attempt].\n")
        score -= 0.1
        if step < 2:
            return (FAIL_INCORRECT, max(0,score))
    else:
        badin = None
        for pos in range(len(tests.asserted['assert_equals'])):
            pair = tests.asserted['assert_equals'][pos]
            input = tests.tested[function][pos]
            if pair[0] != pair[1] and encoder(input) >= 0:
                badin = input
        if not badin is None:
            outp.write("The test for %s with input %s has incorrect output.\n" % (repr(function), repr(badin)))
            score -= 0.3
            if step < 2:
                return (FAIL_INCORRECT, max(0,score))
    
    results = [0]*len(REASONS)
    # Look for proper coverage
    for input in tests.tested[function]:
        code = encoder(input)
        if code == -1:
            outp.write("The test input %s violates the precondition of %s.\n" % (repr(input),repr(function)))
            score -= 0.2
            if step < 2:
                return (FAIL_INCORRECT, max(0,score))
        results[code-1] += 1
    for pos in range(len(results)):
        if results[pos] > 1 and pos < len(REASONS):
            outp.write("You have %s cases of %s. (but that is okay)\n" % (repr(results[pos]),REASONS[pos]))
    
    ntests = len(list(filter(lambda x : x > 0, results)))
    if  ntests < wtests:
        outp.write("You only have %d distinct test case%s [wanted %d].\n" % (ntests,'' if ntests == 1 else 's', wtests))
        score -= 0.1* (wtests-ntests)
        if step < 2:
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
    outp.write('Docstring comments:\n')
    status, p1 = grade_docstring(file,1,outp)
    if p1 == 1:
        outp.write('The module docstring looks good.\n\n')
    else:
        outp.write('\n')
    
    if not status:
        outp.write("Test case comments:\n")
        status, p2 = grade_testcases(file,2,outp)
        if p2 == 1:
            outp.write('The test cases look good.\n\n')
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
    return grade_file('test.py',outp)


if __name__ == '__main__':
    print(grade())