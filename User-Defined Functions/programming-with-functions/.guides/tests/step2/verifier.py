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
from modlib import *

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
        Wrapper for introcs.assert_true.
        
        Allow it to be interchanged with assert_equals.
        """
        if not 'assert_equals' in self._asserts:
            self._asserts['assert_equals'] = []
        self._asserts['assert_equals'].append((True,received))
    
    def assert_false(self,received,message=None):
        """
        Wrapper for introcs.assert_false
        
        Allow it to be interchanged with assert_equals.
        """
        if not 'assert_equals' in self._asserts:
            self._asserts['assert_equals'] = []
        self._asserts['assert_equals'].append((False,received))
    
    def assert_floats_equal(self, expected, received,message=None):
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
    
    def matching_parens1(self,s):
        """
        Incorrect version for first pass
        """
        if not 'matching_parens' in self._tests:
            self._tests['matching_parens'] = []
        self._tests['matching_parens'].append(s)
        return 2 if self.matching_parens3(s) else 1
    
    def matching_parens2(self,s):
        """
        Correct version
        """
        self._environment.print('___test___')
        if not 'matching_parens' in self._tests:
            self._tests['matching_parens'] = []
        self._tests['matching_parens'].append(s)
        return self.matching_parens3(s)
    
    def matching_parens3(self,s):
        """
        Correct version, no logging
        """
        first = s.find('(')
        secnd = s.find(')',first)
        return first != -1 and secnd != -1
    
    def first_in_parens1(self,s):
        """
        Incorrect version for first pass
        """
        if not 'first_in_parens' in self._tests:
            self._tests['first_in_parens'] = []
        self._tests['first_in_parens'].append(s)
        return self.first_in_parens3(s)+'xxx'
    
    def first_in_parens2(self,s):
        """
        Correct version
        """
        self._environment.print('___test___')
        if not 'first_in_parens' in self._tests:
            self._tests['first_in_parens'] = []
        self._tests['first_in_parens'].append(s)
        return self.first_in_parens3(s)
    
    def first_in_parens3(self,s):
        """
        Correct version, no logging
        """
        first = s.find('(')
        secnd = s.find(')',first)
        return s[first+1:secnd]

pass
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
            func = types.ModuleType('funcs')
            if step:
                func.matching_parens = testplan.matching_parens2
                func.first_in_parens = testplan.first_in_parens2
            else:
                func.matching_parens = testplan.matching_parens1
                func.first_in_parens = testplan.first_in_parens1
            environment.capture('funcs',func)
        else:
            try:
                func = load_from_path('funcs',WORKSPACE)
                func.print = environment.print
                func.input = environment.input
                environment.capture('funcs',func)
            except:
                pass
        
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


pass
#mark -
#mark Test Case Checking
def encode_matching_parens(input):
    """
    Returns: the hash encoding for input to matching_parens
    
    Parameter input: The input to matching_parens
    Precondition: s is a string
    """
    if type(input) != str:
        return -1
    
    if len(input) == 0:
        return 1
    
    left = input.find('(')
    rght = input.find(')')
    if left == -1 and rght == -1:
        return 2
    elif left == -1:
        return 3
    elif rght == -1:
        return 4
    
    if rght < left:
        next = input.find(')',left)
        if next == -1:
            return 5
        else:
            return 6
    else:
        next1 = input.find('(',left+1)
        next2 = input.find(')',rght+1)
        if next1 == -1 and next2 == -1:
            return 7
        elif next1 == -1 or next2 == -1:
            return 8
        elif next1 < rght:
            return 9
        elif next1 < next2:
            return 10
    
    return 11


def encode_first_in_parens(input):
    """
    Returns: the hash encoding for input to first_in_parens
    
    Parameter input: The input to first_in_parens
    Precondition: s is a string with matching parens
    """
    if type(input) != str:
        return -1
    
    left = input.find('(')
    rght = input.find(')',left+1)
    if left == -1 or rght == -1:
        return -1
    
    output = input[left+1:rght]
    if input.count('(') == 1 and input.count(')') == 1:
        if output == '':
            return 2
        elif output == input[1:-1]:
            return 3
        else:
            return 1
    else:
        close = input.find(')')
        if close < left:
            return 4
        
        left2 = input.find('(',left+1)
        rght2 = input.find(')',rght+1)
        if left2 != -1 and rght2 != -1:
            if left2 > rght and left2 < rght2:
                return 5
            elif left2 < rght2:
                return 6
    return 7


# The explanatory reasons for the tests
MATCHING_PARENS = [
    "a test on the empty string ''",
    "a basic test with no parentheses",
    "a test with no open parenthesis '('",
    "a test with no close parenthesis ')'",
    "a test with the order of parentheses reversed",
    "a matching test with an early close parenthesis ')'",
    "a basic matching test with one pair of parentheses",
    "a matching test with a stray later parenthesis",
    "a matching test with nested parentheses",
    "a matching test with multiple pairs of parentheses",
    "a complex test with multiple stray parentheses"
]

FIRST_IN_PARENS = [
    "a basic test with one pair of parentheses (something inside the parentheses, something outside)",
    "a test with one pair of parentheses, and nothing inside them",
    "a test with one pair of parentheses, and nothing outside them",
    "a test with a closed parenthesis before an open",
    "a test with two sequential pairs of parentheses",
    "a test with two nested pairs of parentheses",
    "a complex test with unmatching parentheses"
]


pass
#mark -
#mark Subgraders
def grade_first_in_parens(file,step=0,outp=sys.stdout):
    """
    Returns the test result and score for the test cases for first_in_parens
    
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
    env, tests = import_module(file,0)
    if type(env) == str:
        outp.write(env)
        return (FAIL_CRASHES,0)
    
    # Step 1
    score = 1
    if not hasattr(env.module,'introcs'):
        outp.write("File %s does not imported 'introcs' as instructed.\n" % repr(file))
        return (FAIL_INCORRECT,0)
    elif not hasattr(env.module,'funcs'):
        outp.write("File %s does not imported 'funcs' as instructed.\n" % repr(file))
        return (FAIL_INCORRECT,0)
    elif not hasattr(env.module,'test_first_in_parens'):
        outp.write("File %s is missing the header for 'test_first_in_parens'.\n" % repr(file))
        return (FAIL_INCORRECT, 0)
    
    env.reset()
    tests.reset()
    env.module.test_first_in_parens()
    
    if not 'first_in_parens' in tests.tested:
        outp.write("You have not called the function 'first_in_parens' properly.\n")
        return (FAIL_INCORRECT,0)
    
    if not 'assert_equals' in tests.asserted or len(tests.asserted['assert_equals']) != len(tests.tested['first_in_parens']):
        outp.write("You were supposed to call 'assert_equals', 'assert_true', or 'assert_false' for each test case.\n")
        score -= 0.1
        if not step:
            return (FAIL_INCORRECT, max(0,score))
    
    badin = None
    for pos in range(len(tests.asserted['assert_equals'])):
        if  pos < len(tests.tested['first_in_parens']):
            pair  = tests.asserted['assert_equals'][pos]
            input = tests.tested['first_in_parens'][pos]
            if pair[0] != tests.first_in_parens3(input) and encode_first_in_parens(input) >= 0:
                badin = input
    
    if badin:
        outp.write("In 'assert_equals', the expected value goes first [see %s].\n" % repr(badin))
        score -= 0.1
        if not step:
            return (FAIL_BAD_STYLE,0)
    
    env, tests = import_module(file,1)
    if type(env) == str:
        outp.write(env)
        return (FAIL_CRASHES,0)
    
    env.reset()
    tests.reset()
    env.module.test_first_in_parens()
    badin = None
    for pos in range(len(tests.asserted['assert_equals'])):
        pair = tests.asserted['assert_equals'][pos]
        input = tests.tested['first_in_parens'][pos]
        if pair[0] != pair[1] and encode_first_in_parens(input) >= 0:
            badin = tests.tested['first_in_parens'][pos]
        if not badin is None:
            outp.write("The test for input %s has incorrect output.\n" % repr(badin))
            score -= 0.3
            if not step:
                return (FAIL_INCORRECT, max(0,score))
    
    # Look for proper coverage
    results = [0]*len(FIRST_IN_PARENS)
    for input in tests.tested['first_in_parens']:
        code = encode_first_in_parens(input)
        if code == -1:
            outp.write("The test first_in_parens(%s) violates the precondition.\n" % repr(input))
            score -= 0.2
            if not step:
                return (FAIL_INCORRECT, max(0,score))
        results[code-1] += 1
    for pos in range(len(results)):
        if results[pos] > 1 and pos < len(FIRST_IN_PARENS):
            outp.write("You have %s cases of %s for 'first_in_parens' (but that is okay).\n" % (repr(results[pos]),FIRST_IN_PARENS[pos]))
        
    ntests = len(list(filter(lambda x : x > 0, results)))
    wtests = 5
    if  ntests < wtests:
        outp.write("There are only %d distinct test case%s for 'first_in_parens' [wanted %d].\n" % (ntests,'' if ntests == 1 else 's', wtests))
        score -= 0.1* (wtests-ntests)
        if not step:
            return (FAIL_INCORRECT, max(0,score))
    
    return (TEST_SUCCESS, max(0,score))


def grade_matching_parens(file,step=0,outp=sys.stdout):
    """
    Returns the test result and score for the test cases for matching_parens
    
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
    env, tests = import_module(file,0)
    if type(env) == str:
        outp.write(env)
        return (FAIL_CRASHES,0)
    
    # Step 1
    score = 1
    if not hasattr(env.module,'introcs'):
        outp.write("File %s does not imported 'introcs' as instructed.\n" % repr(file))
        return (FAIL_INCORRECT,0)
    elif not hasattr(env.module,'funcs'):
        outp.write("File %s does not imported 'funcs' as instructed.\n" % repr(file))
        return (FAIL_INCORRECT,0)
    elif not hasattr(env.module,'test_matching_parens'):
        outp.write("File %s is missing the header for 'test_matching_parens'.\n" % repr(file))
        return (FAIL_INCORRECT, 0)
    
    env.reset()
    tests.reset()
    env.module.test_matching_parens()
    
    if not 'matching_parens' in tests.tested:
        outp.write("You have not called the function 'matching_parens' properly.\n")
        return (FAIL_INCORRECT,0)
    
    if not 'assert_equals' in tests.asserted or len(tests.asserted['assert_equals']) != len(tests.tested['matching_parens']):
        outp.write("You were supposed to call 'assert_equals', 'assert_true', or 'assert_false' for each test case.\n")
        score -= 0.1
        if not step:
            return (FAIL_INCORRECT, max(0,score))
    
    badin = None
    for pos in range(len(tests.asserted['assert_equals'])):
        if  pos < len(tests.tested['matching_parens']):
            pair  = tests.asserted['assert_equals'][pos]
            input = tests.tested['matching_parens'][pos]
            if pair[0] != tests.matching_parens3(input) and encode_matching_parens(input) >= 0:
                badin = input
    
    if badin:
        outp.write("In 'assert_equals', the expected value goes first [see %s].\n" % repr(badin))
        score -= 0.1
        if not step:
            return (FAIL_BAD_STYLE,0)
    
    env, tests = import_module(file,1)
    if type(env) == str:
        outp.write(env)
        return (FAIL_CRASHES,0)
    
    env.reset()
    tests.reset()
    env.module.test_matching_parens()
    badin = None
    for pos in range(len(tests.asserted['assert_equals'])):
        pair = tests.asserted['assert_equals'][pos]
        input = tests.tested['matching_parens'][pos]
        if pair[0] != pair[1] and encode_first_in_parens(input) >= 0:
            badin = tests.tested['matching_parens'][pos]
        if not badin is None:
            outp.write("The test for input %s has incorrect output.\n" % repr(badin))
            score -= 0.3
            if not step:
                return (FAIL_INCORRECT, max(0,score))
    
    # Look for proper coverage
    results = [0]*len(MATCHING_PARENS)
    for input in tests.tested['matching_parens']:
        code = encode_matching_parens(input)
        if code == -1:
            outp.write("The test matching_parens(%s) violates the precondition.\n" % repr(input))
            score -= 0.2
            if not step:
                return (FAIL_INCORRECT, max(0,score))
        else:
            results[code-1] += 1
    for pos in range(len(results)):
        if results[pos] > 1 and pos < len(MATCHING_PARENS):
            outp.write("You have %s cases of %s for 'matching_parens' (but that is okay).\n" % (repr(results[pos]),MATCHING_PARENS[pos]))
        
    ntests = len(list(filter(lambda x : x > 0, results)))
    wtests = 7
    if  ntests < wtests:
        outp.write("There are only %d distinct test case%s for 'matching_parens' [wanted %d].\n" % (ntests,'' if ntests == 1 else 's', wtests))
        score -= 0.1* (wtests-ntests)
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
    outp.write("Procedure 'test_matching_parens' comments:\n")
    status, p1 = grade_matching_parens(file,1,outp)
    if p1 == 1:
        outp.write("The tests for 'matching_parens' look good.\n\n")
    else:
        outp.write('\n')
    
    if not status:
        outp.write("Procedure 'test_first_in_parens' comments:\n")
        status, p2 = grade_first_in_parens(file,1,outp)
        if p2 == 1:
            outp.write("The tests for 'first_in_parens' look good.\n\n")
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
    return grade_file('tests.py',outp)


if __name__ == '__main__':
    print(grade())