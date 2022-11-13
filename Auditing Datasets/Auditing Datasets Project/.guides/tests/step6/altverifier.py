"""
The verification functions for Course 6 scripts

This file is insecurely available to students, but if they find it and modify it, they
really did not need this course.

Author: Walker M. White
Date:   November 19, 2019
"""
import os, os.path, sys
import importlib, importlib.util
import traceback
import inspect
import builtins
import ast
import json
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


WORKSPACE = [os.path.expanduser('~'),'workspace']
TESTFILES = WORKSPACE+['.guides','tests','testfiles']


#mark -
#mark MODULE INTERCEPTION
class ProxyModule(object):
    """Parent class of all proxies"""
    
    def __init__(self):
        self.active = {}

class Violations(ProxyModule):
    """This proxy for the violations module cuts down on testing overhead"""
    ACTIVE = False
    LENGTH = 5
    
    def bad_visibility(self,visibility,minimum):
        """Unimplemented function"""
        raise NotImplementedError('violations.bad_visibility')
    
    def bad_winds(self,winds,maxwind,maxcross):
        """Unimplemented function"""
        raise NotImplementedError('violations.bad_winds')
    
    def bad_ceiling(self,ceiling,minimum):
        """Unimplemented function"""
        raise NotImplementedError('violations.bad_ceiling')
    
    def get_weather_report(self,takeoff,weather):
        """Unimplemented function"""
        raise NotImplementedError('violations.get_weather_report')
    
    def get_weather_violation(self,weather,minimums):
        """Unimplemented function"""
        raise NotImplementedError('violations.get_weather_violation')
    
    def list_weather_violations(self,directory):
        """Captured function for testing"""
        Violations.ACTIVE = True
        result = [['S00687','548QR','I061','2017-01-08T14:00:00-05:00','2017-01-08T16:00:00-05:00','VFR','Pattern','Winds'],
                  ['S00758','548QR','I072','2017-01-08T09:00:00-05:00','2017-01-08T11:00:00-05:00','VFR','Pattern','Visibility'],
                  ['S00880','133CZ','I072','2017-01-08T14:00:00-05:00','2017-01-08T16:00:00-05:00','VFR','Pattern','Winds'],
                  ['S00971','426JQ','I072','2017-01-12T13:00:00-05:00','2017-01-12T15:00:00-05:00','VFR','Pattern','Ceiling'],
                  ['S00922','133CZ','I053','2017-01-18T11:00:00-05:00','2017-01-18T13:00:00-05:00','VFR','Practice Area','Weather']]
        return result[:self.LENGTH]


class Endorsements(object):
    """This proxy for the endorsments module cuts down on testing overhead"""
    ACTIVE = False
    LENGTH = 5
    
    def teaches_multiengine(self,instructor):
        """Unimplemented function"""
        raise NotImplementedError('endorsements.teaches_multiengine')
    
    def teaches_instrument(self,instructor):
        """Unimplemented function"""
        raise NotImplementedError('endorsements.teaches_instrument')
    
    def is_advanced(self,plane):
        """Unimplemented function"""
        raise NotImplementedError('endorsements.is_advanced')
    
    def is_multiengine(self,plane):
        """Unimplemented function"""
        raise NotImplementedError('endorsements.is_multiengine')
    
    def is_ifr_capable(self,plane):
        """Unimplemented function"""
        raise NotImplementedError('endorsements.is_ifr_capable')
    
    def bad_endorsement(self,takeoff,student,instructor,plane):
        """Unimplemented function"""
        raise NotImplementedError('endorsements.bad_endorsement')
    
    def bad_ifr(self,takeoff,student,instructor,plane):
        """Unimplemented function"""
        raise NotImplementedError('endorsements.bad_ifr')
    
    def list_endorsement_violations(self,directory):
        """Captured function for testing"""
        Endorsements.ACTIVE = True
        result = [['S00811','811AX','I077','2017-01-07T10:00:00-05:00','2017-01-07T12:00:00-05:00','IFR','Pattern','IFR'],
                  ['S00526','446BU','',    '2017-01-16T08:00:00-05:00','2017-01-16T10:00:00-05:00','VFR','Practice Area','Endorsement'],
                  ['S00850','426JQ','I032','2017-01-17T14:00:00-05:00','2017-01-17T16:00:00-05:00','IFR','Pattern','IFR']]
        return result[:self.LENGTH]


class Inspections(object):
    """This proxy for the inspections module cuts down on testing overhead"""
    ACTIVE = False
    LENGTH = 5
    
    def list_inspection_violations(self,directory):
        """Captured function for testing"""
        Inspections.ACTIVE = True
        result = [['S00990','684TM','',    '2017-11-09T12:00:00-05:00','2017-11-09T15:00:00-05:00','VFR','Practice Area','Inspection'],
                  ['S00722','738GG','I061','2017-11-10T09:00:00-05:00','2017-11-12T12:00:00-05:00','VFR','Practice Area','Annual'],
                  ['S01161','738GG','I072','2017-11-12T14:00:00-05:00','2017-11-12T16:00:00-05:00','VFR','Pattern','Grounded']]
        return result[:self.LENGTH]


class Execution(object):
    """This proxy for the tests module cuts down on testing overhead"""
    
    def __init__(self):
        """Keep track of what methods are called."""
        self.called = {}
    
    def reset(self):
        """Reset the calls"""
        self.called = {}
    
    def test_app(self):
        """Captured function for testing"""
        self.called['test_app'] = True
    
    def test_utils(self):
        """Captured function for testing"""
        self.called['test_utils'] = True
    
    def test_pilots(self):
        """Captured function for testing"""
        self.called['test_pilots'] = True
    
    def test_violations(self):
        """Captured function for testing"""
        self.called['test_violations'] = True
    
    def test_endorsements(self):
        """Captured function for testing"""
        self.called['test_violations'] = True
    
    def test_inspections(self):
        """Captured function for testing"""
        self.called['test_inspections'] = True
    
    def test_all(self):
        """Captured function for testing"""
        self.called['test_all'] = True
    
    def discover_violations(self,directory,output):
        """Captured function for testing"""
        self.called['discover_violations'] = (directory,output)


pass
#mark -
#mark Helpers
DEPENDENCIES = ['utils']
PROXIES = {'violations':Violations(), 'endorsements':Endorsements(),
           'inspections':Inspections(), 'tests':Execution()}


def import_module(package,name,step=0):
    """
    Returns a reference to the module.
    
    Returns an error message if it fails.
    
    Parameter name: The module name
    Precondition: name is a string
    """
    # BOOTSTRAP
    import types
    depends = {}
    for item in DEPENDENCIES:
        try:
            environment = Environment(item,WORKSPACE+[package])
            for mod in depends:
                environment.capture(mod,depends[mod])
            if not environment.execute():
                message = 'Unable to import %s:\n' % item
                message = message+'\n'.join(environment.printed)+'\n'
                return message
            depends[item] = environment.module
        except Exception as e:
            msg = traceback.format_exc(0)
            pos2 = msg.find('^')
            pos1 = msg.rfind(')',0,pos2)
            if 'SyntaxError: unexpected EOF' in msg or 'IndentationError' in msg:
                msg = 'Remember to include and indent the docstring properly.\n'+msg
            elif pos1 != -1 and pos2 != -1 and not msg[pos1+1:pos2].strip():
                msg = 'Remember to end the header with a colon.\n'+msg
            else:
                msg = ("File %s has a major syntax error.\n" % repr(item+'.py'))+msg
            return msg
    try:
        refs = os.path.splitext(name)[0]
        environment = Environment(refs,WORKSPACE+[package])
        for mod in depends:
            environment.capture(mod,depends[mod])
        for mod in PROXIES:
                environment.capture(mod,PROXIES[mod])
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
            msg = ("File %s has a major syntax error.\n" % repr(item+'.py'))+msg
        return msg

# Localized error codes
def get_docstring(module):
    """
    Returns the module docstring as a list of lines
    
    If there is no docstring, this function returns None.
    
    Parameter module: The module
    Precondition: module is a ModuleType object
    """
    if module.__doc__ is None:
        return None
    
    lines = module.__doc__.split('\n')
    lines = list(map(lambda x: x.strip(),lines))
    
    start = -1
    for pos in range(len(lines)):
        if lines[pos].strip():
            start = pos
            break
    
    if start == -1:
        return []
    
    end = -1
    for pos in range(1,len(lines)-start):
        if lines[len(lines)-pos].strip():
            end = len(lines)-pos
            break
    
    if end == -1:
        return []
    
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


def check_execute_error(lines,value):
    """
    Returns feedback if the execution error message is wrong
    """
    correct = 'Usage: python auditor dataset [output.csv]'
    message = None
    if len(lines) == 0:
        message = 'execute(%s) did not print out an error message' % repr(value)
    elif len(lines) > 1:
        message = 'execute(%s) printed more than one line' % repr(value)
    elif lines[0] != correct:
        message = 'execute(%s) did not print the error message %s' % (repr(value),repr(correct))
    return message


pass
#mark -
#mark Subgraders
def grade_docstring(package,module,step=0,outp=sys.stdout):
    """
    Returns the test result and score for the docstring.
    
    The step parameter is the phase in the grading pass.  Step 0 is a verification step
    and will stop at the first error found.  Otherwise it will continue through and try 
    to find all errors.
    
    Parameter package: The application package
    Precondition: package is a string
    
    Parameter module: The module to grade
    Precondition: module is a string
    
    Parameter step: The current verfication/grading step
    Precondition: grade is 0 or 1
    
    Parameter outp: The output stream
    Precondition: outp is a stream writer
    """
    env = import_module(package,module)
    if type(env) == str:
        outp.write(env)
        return (FAIL_CRASHES, 0)
    
    score = 1
    module = env.module
    docs = get_docstring(module)
    
    if type(docs) is None:
        outp.write('There is no module docstring in %s.\n' % repr(module))
        return (FAIL_BAD_STYLE,0)
    elif not docs:
        outp.write('The docstring for %s is empty.\n' % repr(module))
        return (FAIL_BAD_STYLE,0)
    
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


def grade_func1(package,module,step=0,outp=sys.stdout):
    """
    Returns the test result and score for the implementation of discover_violations
    
    The step parameter is the phase in the grading pass.  Step 0 is a verification step
    and will stop at the first error found.  Otherwise it will continue through and try 
    to find all errors.
    
    Parameter package: The application package
    Precondition: package is a string
    
    Parameter module: The module to grade
    Precondition: module is a string
    
    Parameter step: The current verfication/grading step
    Precondition: grade is 0 or 1
    
    Parameter outp: The output stream
    Precondition: outp is a stream writer
    """
    score = 1
    env = import_module(package,module)
    function = 'discover_violations'    

    # Add extra newline to ensure the message lines up with the green/red result symbol
    outp.write("\n")
    
    if type(env) == str:
        outp.write(env)
        return (FAIL_CRASHES, 0)
    elif not hasattr(env.module,function):
        outp.write("File %s is missing the header for %s.\n" % (repr(module),repr(function)))
        return (FAIL_INCORRECT, 0)
    else:
        for item in DEPENDENCIES:
            if not hasattr(env.module,item):
                outp.write("File %s is does not import %s.\n" % (repr(module),repr(item)))
                return (FAIL_INCORRECT, 0)
    
    utils  = env.module.utils
    fpath = os.path.join(*TESTFILES)
    npath = repr('directory')
    func = getattr(env.module,function)
    try:
        env.reset()
        func(fpath,None)
        amnt = len(PROXIES['violations'].list_weather_violations(None))
        amnt += len(PROXIES['endorsements'].list_endorsement_violations(None))
        amnt += len(PROXIES['inspections'].list_inspection_violations(None))
        expect = '%s violations found.' % str(amnt)
        if not env.printed:
            outp.write("%s(%s,None) did not print the number of violations found.\n" % (function,npath))
            score -= 0.2
            if not step:
                return (FAIL_INCORRECT, max(0,score))
        elif len(env.printed) > 1:
            outp.write("%s(%s,None) printed more than one line.\n"  % (function,npath))
            score -= 0.2
            if not step:
                return (FAIL_INCORRECT, max(0,score))
        elif env.printed[0].strip() == expect[:-1]:
            outp.write("%s(%s,None) is missing a period from its printed output.\n"  % (function,npath))
            score -= 0.2
            if not step:
                return (FAIL_INCORRECT, max(0,score))
        elif env.printed[0].strip() != expect:
            data = (function,npath,repr(env.printed[0].strip()),repr(expect))
            outp.write("%s(%s,None)  printed %s, not %s.\n"  % data)
            score -= 0.2
            if not step:
                return (FAIL_INCORRECT, max(0,score))
    except NotImplementedError as e:
        outp.write('The body of %s uses %s, which should not be used here.\n' % (function,e.args[0]))
        score -= 0.2
        if not step:
            return (FAIL_INCORRECT, max(0,score))
    except:
        import traceback
        outp.write("The call %s(%s,None) crashed.\n" % (function,npath))
        outp.write(traceback.format_exc()+'\n')
        score -= 0.2
        if not step:
            return (FAIL_INCORRECT, max(0,score))
 
    Violations.LENGTH   = 5
    Endorsements.LENGTH = 5
    Inspections.LENGTH  = 5
    opath  = os.path.join(*TESTFILES,'temp.csv')
    try:
        env.reset()
        func(fpath,opath)
        amnt = len(PROXIES['violations'].list_weather_violations(None))
        amnt += len(PROXIES['endorsements'].list_endorsement_violations(None))
        amnt += len(PROXIES['inspections'].list_inspection_violations(None))
        expect = '%s violations found.' % str(amnt)
        if not env.printed:
            outp.write("%s(%s,%s) did not print the number of violations found.\n" % (function,npath,repr(opath)))
            score -= 0.1
            if not step:
                return (FAIL_INCORRECT, max(0,score))
        elif len(env.printed) > 1:
            outp.write("%s(%s,%s) printed more than one line.\n"  % (function,npath,repr(opath)))
            score -= 0.1
            if not step:
                return (FAIL_INCORRECT, max(0,score))
        elif env.printed[0].strip() == expect[:-1]:
            outp.write("%s(%s,%s) is missing a period from its printed output.\n"  % (function,npath,repr(opath)))
            score -= 0.1
            if not step:
                return (FAIL_INCORRECT, max(0,score))
        elif env.printed[0].strip() != expect:
            data = (function,npath,repr(opath),repr(env.printed[0].strip()),repr(expect))
            outp.write("%s(%s,%s)  printed %s, not %s.\n"  % data)
            score -= 0.2
            if not step:
                return (FAIL_INCORRECT, max(0,score))
        
        if not os.path.exists(opath):
            outp.write("%s(%s,%s) did create the file %s.\n" % (function,npath,repr(opath)))
            score -= 0.5
            if not step:
                return (FAIL_INCORRECT, max(0,score))
        
        try:
            data = utils.read_csv(opath)
        except:
            data = None
        
        if data is None:
            outp.write("The file %s could not be read. Make sure it has the right format.\n" % repr(opath))
            score -= 0.5
            if not step:
                return (FAIL_INCORRECT, max(0,score))
        elif len(data) == 0:
            outp.write("The file %s is empty.\n" % repr(output))
            score -= 0.5
            if not step:
                return (FAIL_INCORRECT, max(0,score))
        else:
            header1 = ['STUDENT','AIRPLANE','INSTRUCTOR','TAKEOFF','LANDING','FILED','AREA','REASON']
            header2 = list(map(lambda x: x.upper(),data[0]))
            if header2 != header1:
                outp.write('The header for %s is %s, not %s.\n' % (repr(opath),header1,header2))
                score -= 0.1
                if not step:
                    return (FAIL_INCORRECT, max(0,score))
            
            # Hash the student answers for comparison
            found = {}
            for item in data[1:]:
                found[item[0]+item[3]] = item
            
            weather = PROXIES['violations'].list_weather_violations(None)
            data = {}
            for item in weather:
                data[item[0]+item[3]] = item
            weather = data
            
            pilots = PROXIES['endorsements'].list_endorsement_violations(None) if Endorsements.ACTIVE else []
            data = {}
            for item in pilots:
                data[item[0]+item[3]] = item
            pilots = data
            
            planes = PROXIES['inspections'].list_inspection_violations(None) if Inspections.ACTIVE else []
            data = {}
            for item in planes:
                data[item[0]+item[3]] = item
            planes = data
            
            for key in weather:
                if not key in found:
                    data = (repr(opath),weather[key][3],weather[key][0])
                    outp.write('File %s is missing the bad weather flight %s for pilot %s.\n' % data)
                    score -= 0.5/amnt
                    if not step:
                        return (FAIL_INCORRECT, max(0,score))
                    
            isbad = False
            for key in pilots:
                if not key in found:
                    data = (repr(opath),pilots[key][3],pilots[key][0])
                    outp.write('File %s is missing the bad endorsement flight %s for pilot %s.\n' % data)
                    isbad = True
            if isbad:
                outp.write('Consider removing the endorsement extension if you cannot get it right.\n\n')
                
            if Inspections.ACTIVE:
                isbad = False
                for key in planes:
                    if not key in found:
                        data = (repr(opath),planes[key][3],planes[key][0])
                        outp.write('File %s is missing the bad inspection flight %s for pilot %s.\n' % data)
                        isbad = True
                if isbad:
                    outp.write('Consider removing the inspection extension if you cannot get it right.\n\n')
            
            for key in found:
                match = key in weather
                match = match or key in pilots
                match = match or key in planes
                if not match:
                    data = (repr(opath),found[key][3],found[key][0])
                    outp.write('File %s identified flight %s for pilot %s, even though it is okay.\n' % data)
                    score -= 0.5/amnt
                    if not step:
                        return (FAIL_INCORRECT, max(0,score))
            
            for key in found:
                reason2 = found[key][-1]
                reason1 = None
                if key in weather:
                    reason1 = weather[key][-1]
                elif key in pilots:
                    reason1 = pilots[key][-1]
                elif key in planes:
                    reason1 = planes[key][-1]
                if reason1 != reason2:
                    data = (repr(opath),found[key][3],found[key][0],repr(reason1),repr(reason2))
                    outp.write("File %s identified flight %s for pilot %s as %s, not %s" % data)
                    score -= 0.5/amnt
                    if not step:
                        return (FAIL_INCORRECT, max(0,score))
    except NotImplementedError as e:
        outp.write('The body of %s uses %s, which should not be used here.\n' % (function,e.args[0]))
        score -= 0.5
        if not step:
            return (FAIL_INCORRECT, max(0,score))
    except:
        import traceback
        outp.write("The call %s(%s,%s) crashed.\n" % (function, npath, repr(opath)))
        outp.write(traceback.format_exc()+'\n')
        score -= 0.5
        if not step:
            return (FAIL_INCORRECT, max(0,score))    
    
    return (TEST_SUCCESS,max(0,score))


def grade_func2(package,module,step=0,outp=sys.stdout):
    """
    Returns the test result and score for the implementation of execute
    
    The step parameter is the phase in the grading pass.  Step 0 is a verification step
    and will stop at the first error found.  Otherwise it will continue through and try 
    to find all errors.
    
    Parameter package: The application package
    Precondition: package is a string
    
    Parameter module: The module to grade
    Precondition: module is a string
    
    Parameter step: The current verfication/grading step
    Precondition: grade is 0 or 1
    
    Parameter outp: The output stream
    Precondition: outp is a stream writer
    """
    score = 1
    env = import_module(package,module)
    function = 'execute'
    
    if type(env) == str:
        outp.write(env)
        return (FAIL_CRASHES, 0)
    elif not hasattr(env.module,function):
        outp.write("File %s is missing the header for %s.\n" % (repr(module),repr(function)))
        return (FAIL_INCORRECT, 0)
    else:
        for item in DEPENDENCIES:
            if not hasattr(env.module,item):
                outp.write("File %s is does not import %s.\n" % (repr(module),repr(item)))
                return (FAIL_INCORRECT, 0)
    
    # Test out the error messages
    failures = [[],['input.csv','--test'],['--test','input.csv'],
                ['input.csv','output.csv','--test'],['input.csv','--test','output.csv'],
                ['--test','input.csv','output.csv'],['input.csv','output.csv','extra.csv']]
    
    proxy = PROXIES['tests']
    env.module.discover_violations = proxy.discover_violations
    func = getattr(env.module,function)
    for fail in failures:
        try:
            env.reset()
            func(fail)
            message = check_execute_error(env.printed,fail)
            if not message is None:
                outp.write(message+'\n')
                score -= 0.3/len(failures)
                if not step:
                    return (FAIL_INCORRECT, max(0,score))
        except:
            import traceback
            outp.write("The call %s(%s) crashed.\n" % (function, repr(fail)))
            outp.write(traceback.format_exc()+'\n')
            score -= 0.3/len(failures)
            if not step:
                return (FAIL_INCORRECT, max(0,score))
    env.reset()
    
    value = ['--test']
    printed = False
    try:
        proxy.reset()
        func(value)
        bad = False
        if len(proxy.called) == 0:
            printed 
            outp.write("%s(%s) did not call a test procedure.\n" % (function,repr(value)))
            bad = True
        elif len(proxy.called) > 1:
            outp.write("%s(%s) did more than just call 'test_all'.\n" % (function,repr(value)))
            bad = True
        elif 'discover_violations' in proxy.called:
            outp.write("%s(%s) ran 'discover_violations' when it should have been testing.\n" % (function,repr(value)))
            bad = True
        elif not 'test_all' in proxy.called:
            outp.write("%s(%s) ran a test procedure other than 'test_all'.\n" % (function,repr(value)))
            bad = True
        if bad:
            score -= 0.3
            if not step:
                return (FAIL_INCORRECT, max(0,score))
        if len(env.printed) != 0:
            printed = True
    except:
        import traceback
        outp.write("The call %s(%s) crashed.\n" % (function, repr(value)))
        outp.write(traceback.format_exc()+'\n')
        score -= 0.3
        if not step:
            return (FAIL_INCORRECT, max(0,score))
    
    value = ['input.csv',None]
    try:
        proxy.reset()
        func(value)
        bad = False
        if len(proxy.called) == 0:
            outp.write("%s(%s) did not call 'discover_violations'.\n" % (function,repr(value)))
            bad = True
        elif len(proxy.called) > 1:
            outp.write("%s(%s) did more than just call 'discover_violations'.\n" % (function,repr(value)))
            bad = True
        elif not 'discover_violations' in proxy.called:
            outp.write("%s(%s) called a test procedure when it should have called 'discover_violations'.\n" % (function,repr(value)))
            bad = True
        else:
            args = proxy.called['discover_violations']
            if args[0] != value[0] or args[1] != value[1]:
                outp.write("%s(%s) called discover_violations%s with the wrong arguments (expected %s).\n" % (function,repr(value), repr(args), repr(tuple(value))))
                bad = True
        if bad:
            score -= 0.3
            if not step:
                return (FAIL_INCORRECT, max(0,score))
        if len(env.printed) != 0:
            printed = True
    except:
        import traceback
        outp.write("The call %s(%s) crashed.\n" % (function, repr(value)))
        outp.write(traceback.format_exc()+'\n')
        score -= 0.3
        if not step:
            return (FAIL_INCORRECT, max(0,score))
    
    value = ['input.csv','output.csv']
    try:
        proxy.reset()
        func(value)
        bad = False
        if len(proxy.called) == 0:
            outp.write("%s(%s) did not call 'discover_violations'.\n" % (function,repr(value)))
            bad = True
        elif len(proxy.called) > 1:
            outp.write("%s(%s) did more than just call 'discover_violations'.\n" % (function,repr(value)))
            bad = True
        elif not 'discover_violations' in proxy.called:
            outp.write("%s(%s) called a test procedure when it should have called 'discover_violations'.\n" % (function,repr(value)))
            bad = True
        else:
            args = proxy.called['discover_violations']
            if args[0] != value[0] or args[1] != value[1]:
                outp.write("%s(%s) called discover_violations%s with the wrong arguments (expected %s).\n" % (function,repr(value), repr(args), repr(tuple(value))))
                bad = True
        if bad:
            score -= 0.3
            if not step:
                return (FAIL_INCORRECT, max(0,score))
        if len(env.printed) != 0:
            printed = True
    except:
        import traceback
        outp.write("The call %s(%s) crashed.\n" % (function, repr(value)))
        outp.write(traceback.format_exc()+'\n')
        score -= 0.3
        if not step:
            return (FAIL_INCORRECT, max(0,score))
    
    if printed:
        outp.write('The function %s should only print when the arguments are invalid.\n' % repr(function))
        outp.write('You should remove all debugging print statements from %s.\n' % repr(function))
        score -= 0.1
        if not step:
            return (FAIL_BAD_STYLE,max(0,score))

    return (TEST_SUCCESS,max(0,score))


pass
#mark -
#mark Graders
def grade_module(package,module,outp=sys.stdout):
    """
    Grades the utility package
    
    Parameter package: The application package
    Precondition: package is a string
    
    Parameter module: The module to grade
    Precondition: module is a string
    
    Parameter outp: The output stream
    Precondition: outp is a stream writer
    """
    
    outp.write('Docstring comments:\n')
    status, p = grade_docstring(package,module,1,outp)
    if p == 1:
        outp.write('The module docstring looks good.\n\n')
    else:
        outp.write('\n')
    
    crashes = status
    score = []
    score.append(p)
    
    functions = [('discover_violations',grade_func1),
                 ('execute',            grade_func2)]
    for item in functions:
        if not crashes:
            outp.write("Comments for %s:\n" % repr(item[0]))
            status, p = item[1](package,module,1,outp)
            if p == 1:
                outp.write('The function looks good.\n\n')
            else:
                outp.write('\n')
            score.append(p)
        else:
            score.append(0)
    
    total  = 0.05*score[0]
    factor =  0.95/(len(score)-1)
    for item in score[1:]:
        total += item*factor
    
    return round(total,3)


def grade(outp=sys.stdout):
    """
    Invokes this subgrader (returning a percentage)
    """
    return grade_module('auditor','app.py',outp)


if __name__ == '__main__':
    print(grade())