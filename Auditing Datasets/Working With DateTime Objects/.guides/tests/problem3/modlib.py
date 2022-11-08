"""
Utilities for sandboxing and manipulating modules.

The utilities in this module are typically used by graders, to import and
sandbox student submissions.  That is why this module is internal, and we
have not yet generated Sphinx documentation for it.

:author:  Walker M. White (wmw2)
:version: June 9, 2019
"""
import os.path


def load_from_path(name,path=None):
    """
    Loads the module of the given name in the application directory.
    
    Normally, modules can only be imported if they are in the same directory as
    this one.  The application modules (utils.py, app.py, etc...) are not in the
    folder and cannot be imported.  This function does some python magic to get
    around that problem.
    
    The optional path should be specified as a list of directories. Only relative
    (not absolute) paths are supported.
    
    :param name: The module name (without the .py extension)
    :type name: ``str``
    
    :param path: The file system path to the module (None for working directory)
    :type path: ``list`` of ``str`` or `None`
    """
    assert type(name) == str, '%s is not a string' % repr(name)
    import importlib.util
    import os.path
    full = name+'.py' if path is None else os.path.join(*path,name+'.py')
    assert os.path.isfile(full),'%s is not a valid file' % repr(full)
    
    spec = importlib.util.spec_from_file_location(name,full)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class Environment(object):
    """
    Instance is an execution environment to capture print and input.
    
    Like :func:`load_from_path`, this class can load a module from any path.  However, 
    this is a more powerful all purpose wrapper in that it can intercept all calls to 
    `print` or `input`.  This allows an autograder to grade an assignment with interactive 
    features.  See the method :meth:`enter` for how to add input to the environment
    before executing it.
    
    By default, the environment loads the module as module, not a script.  However, calling
    :meth:`reset` with ``True`` before execution will execute the module as a script
    instead.
    """
    # The maximum number of times we allow a while loop to execute
    LIMIT = 999
    
    @property
    def module(self):
        """
        The module for this environment
        
        **Invariant**: Value is a `module` object.
        """
        return self._mods
    
    @property
    def code(self):
        """
        The code executed in this environment
        
        **Invariant**: Value is a `str`.
        """
        return self._code
    
    @property
    def error(self):
        """
        Whether the most recent execution had an error.
        
        **Invariant**: Value is a `bool`.
        """
        return self._errors
    
    @property
    def printed(self):
        """
        The captured print statements of this environment.
        
        Each call to `print` is a separate entry to this list.  Special
        endlines (or files) are ignored.
        
        **Invariant**: Value is a list of strings.
        """
        return self._prints
    
    @property
    def inputed(self):
        """
        The captured input statements of this environment.
        
        Each call to `input` adds a new element to the list.  Only the
        prompts are added to this list, not the user response (which
        are specified in the initializer).
        
        **Invariant**: Value is a list of strings or None.
        """
        return self._inputs
    
    @property
    def imported(self):
        """
        The captured imports of this environment.
        
        This is used to wrap the imported function for analysis.  It maps a name
        to a preimported (modified) module.
        
        **Invariant**: Value is a dictionary of string-module pairs or None.
        """
        return self._imports
    
    @property
    def files(self):
        """
        The collection of currently open files.
        
        This collection is only contains files that are open.  Once they are
        closed, they are removed from the list.
        
        **Invariant**: Value is a dictionary of strings to open files.
        """
        return self._files
    
    def __init__(self,name,path=None,code=None):
        """
        Initializes the execution evironment
        
        This method prepares the module for execution, but does not actually
        execute it.  You must call the method :meth:`execute` for that. The
        module should either be in the current working directory or be along
        the specified path. However, no error is generated until the module is
        executed. This includes the case in which the file does not exist.
        
        The optional path should be specified as a list of directories. Only
        relative (not absolute) paths are supported.
        
        If code is not None, this module will use that string as the source code
        instead of the contents of the file.  This is true even if the file does
        not exist. However, you should not specify both code and path (e.g. at 
        least one of path or code should be None).
        
        :param name: The module name (without the .py extension)
        :type name: ``str``
        
        :param path: The file system path to the module (None for working directory)
        :type path: ``list`` of ``str`` or ``None``, this initialize will execute 
        the string of code instead
        
        :param code: the source code to execute in place of the file contents
        :type code: ``str``
        """
        assert type(name) == str, '%s is not a string' % repr(name)
        assert path is None or type(path) == list, '%s is an invalid path' % repr(path)
        assert code is None or type(code) == str, '%s is not a string' % repr(code)
        assert path is None or code is None, 'do not specify both path and code' 
        
        from types import ModuleType
        if not path:
            refs = name+'.py'
        else:
            refs = os.path.join(*path,name+'.py')
        
        if code:
            self._code = code
        else:
            try:
                with open(refs) as file:
                    self._code = file.read()
            except:
                self._code = 'raise FileNotFoundError("Cannot find file \'%s\'")' % refs
        
        self._name = name
        self._main = False
        self._mods = ModuleType(name)
        self._path = refs
        self._mods.print = self.print
        self._mods.input = self.input
        self._mods.open  = self.open
        
        self._errors = False
        self._prints = []
        self._inputs = []
        self._values = []
        self._files  = {}
        self._imports = {}
    
    def print(self, *objects, sep=' ', end='\n', file=None, flush=False):
        """
        Prints the given objects, capturing the results internally.
        
        All print statements convert the arguments to a string and store
        these strings in an internal list. Each call to `print` is a separate
        entry to the list.  Special endlines (or files) are ignored.
        
        The parameters agree with the built-in print
        """
        self._prints.append(sep.join(map(str,objects)))
    
    def input(self,prompt=None):
        """
        Records an input request, and returns a predefined value.
        
        Each `input` request is given one of a list of predefined values
        specified by the initializer.  Values are returned in the order
        they were provided. If this list is empty, or it is shorter than
        the number of calls to `input`, subsequent calls will get the empty
        string.
        
        In addition, all calls to input will record the prompt to a internal
        list of strings.
        
        The parameters agree with the built-in input
        """
        self._inputs.append(prompt)
        pos = len(self._inputs)
        if pos <= len(self._values):
            return self._values[pos-1]
        return ''
    
    def open(self, file, mode='r', buffering=-1, encoding=None, errors=None, newline=None, closefd=True, opener=None):
        """
        Opens the given file (with the provided arguments)
        
        This proxy allows us to detect which files have not been closed.  The file
        is recorded and added to self._files.  The close method is reassigned to a 
        proxy (for recording).
        
        The parameters agree with the built-in open
        """
        if file in self._files:
            raise ValueError('File %s is already open.' % repr(file))
        
        result = open(file,mode,buffering,encoding,errors,newline,closefd,opener)
        self._files[file] = result
        method = result.close
        result.close = lambda : self.close_file(file,method)
        return result
    
    def close_file(self,file,closer):
        """
        A proxy for the close method, to detect that a file is closed.
        
        :param main: the file name
        :type main: ``str``
        
        :param closer: the original close method
        :type main: ``callable``
        """
        del self._files[file]
        closer()
    
    def execute(self):
        """
        Returns True if the module environment was executed successfully.
        
        If the module crashes on execution, the error will be recorded using
        the internal print function (in addition to returning false).
        
        It is safe to call this method more than once to reload a module.
        However, if the module has print statements or is input sensitive,
        then it should be reset first.
        """
        try:
            import builtins
            self.orig_import = builtins.__import__
            self._mods.__dict__['__name__'] = ('__main__' if self._main else self._name)
            builtins.__import__ = self.redirect
            compiled = compile(self._code, self._path, 'exec')
            exec(compiled, self._mods.__dict__)
            builtins.__import__ = self.orig_import
            return True
        except:
            import sys
            import traceback
            self._errors = True
            formt = traceback.format_exception(*sys.exc_info())
            mark = -1
            for pairs in enumerate(formt):
                if '<frozen ' in pairs[1]:
                    mark = pairs[0]
            formt = list(map(lambda x : x[:-1],formt[mark+1:]))
            trace = []
            for item in formt:
                trace.extend(item.split('\n')) 
            trace = self._rewrite_trace(trace)
            self._prints.extend(trace)
            return False
    
    def reset(self,main=False):
        """
        Resets all print and input statements.
        
        This method only clears the interactive features.  It does not reload
        the module. The optional argument main allows the reset to change any
        future execution style (module or script)
        
        :param main: whether to reset this module to run as a script
        :type main: ``bool``
        """
        self._main = main
        self._prints = []
        self._inputs = []
        self._errors = False
    
    def capture(self,name,module):
        """
        Capture the given module name and replace it with the given module.
        
        The purpose of this method is to redefine the import command in the module
        associated with this environment. Upon calling :meth:`execute`, any import
        statements for a module of a captured name will replace that module with 
        an assigned proxy.  This is useful for redefining functions for built-in
        modules (such as the unit test functions).
        
        If `module` is None, this will release any captures. When calling :meth:`execute`, 
        the import command will then import the normal module associated with the given
        name.
        
        :param name: The name of the module to capture
        :type name: ``str``
        
        :param module: The proxy module to associate with `name`
        :type module:  ``Module`` or None
        """
        self._imports[name] = module
    
    def redirect(self, name, globals=None, locals=None, fromlist=(), level=0):
        """
        Imports a module of the given name, replacing with proxies as necessary.
        
        This method is a replacement to __import__.  If a module name has been captured,
        it will use the proxy module.  Otherwise, it will use the normal import command
        to handle the module.
        
        The parameters agree with the built-in __import__
        """
        if name in self._imports:
            return self._imports[name]
        return self.orig_import(name,globals,locals,fromlist,level)
    
    def enter(self,*values):
        """
        Enters a set of values to passed to an input function.
        
        The values are a list of predefined inputs (for grading).  These inputs will be 
        provided to any call of the `input` function, in the order they were provided.  
        If there is no list of values, or it is shorter than the number of calls to `input`,
        subsequent calls will get the empty string.
        
        :param values: The list of values for the inputs
        :type values:  ``list`` of ``str``
        """
        self._values = list(map(str,values))