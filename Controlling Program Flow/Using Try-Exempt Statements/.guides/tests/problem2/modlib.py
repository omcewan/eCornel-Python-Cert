"""
Utilities for sandboxing and manipulating modules.

The utilities in this module are typically used by graders, to import and
sandbox student submissions.  That is why this module is internal, and we
have not yet generated Sphinx documentation for it.

:author:  Walker M. White (wmw2)
:version: June 9, 2019
"""
import os.path
import introcs


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
    import importlib.util

    full = name+'.py' if path is None else os.path.join(*path,name+'.py')
    spec = importlib.util.spec_from_file_location(name,full)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class Environment(object):
    """
    Instance is an execution environment to capture print and input.

    Like :func:`load_from_path`, this class can load a function from
    any path.  However, this is a more powerful all purpose wrapper
    in that it can intercept all calls to `print` or `input`.  This
    allows an autograder to grade an assignment with interactive features.
    """

    @property
    def module(self):
        """
        The module for this environment

        **Invariant**: Value is a `module` object.
        """
        return self._mods

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

    def __init__(self,name,path=None,*values):
        """
        Initializes the execution evironment
        
        This method prepares the module for execution, but does not actually
        execute it.  You must call the method :meth:`execute` for that. The
        module should either be in the current working directory or be along
        the specified path. However, no error is generated until the module is
        executed.
        
        The optional path should be specified as a list of directories. Only
        relative (not absolute) paths are supported.
        
        The optional parameter `values` is for specifying a list of predefined
        inputs (for grading).  These inputs will be provided to any call of
        the `input` function, in the order they were provided.  If there is
        no list of values, or it is shorter than the number of calls to `input`,
        subsequent calls will get the empty string.
        
        :param name: The module name (without the .py extension)
        :type name: ``str``
        
        :param path: The file system path to the module (None for working directory)
        :type path: ``list`` of ``str`` or `None`
        
        :param values: The list of values for the inputs
        :type values:  ``list`` of ``str``
        """
        import importlib.util
        if not path:
            refs = name+'.py'
        else:
            import sys
            refs = os.path.join(*path,name+'.py')
            sys.path.append(os.path.join(*path))
        
        self._name = name
        self._spec = importlib.util.spec_from_file_location(name, refs)
        self._mods = importlib.util.module_from_spec(self._spec)
        self._mods.print = self.print
        self._mods.input = self.input
        
        self._errors = False
        self._prints = []
        self._inputs = []
        self._values = list(map(str,values))
        
        # To capture imports
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
    
    def execute(self):
        """
        Returns True if the module environment was executed successfully.
        
        If the module crashes on execution, the error will be recorded using
        the internal print function (in addition to returning false).
        
        It is safe to call this method more than once to reload a module.
        """
        try:
            import builtins
            self.orig_import = builtins.__import__
            builtins.__import__ = self.redirect
            self._spec.loader.exec_module(self._mods)
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
            self._prints.extend(formt)
            return False
    
    def reset(self,main=False):
        """
        Resets all print and input statements.
        
        This method only clears the interactive features.  It does not reload
        the module.
        """
        import importlib.util
        
        if main and self._spec.name != '__main__':
            self._spec = importlib.util.spec_from_file_location('__main__', self._spec.origin)
            self._mods = importlib.util.module_from_spec(self._spec)
            self._mods.print = self.print
            self._mods.input = self.input
        elif not main and self._spec == '__main__':
            self._spec = importlib.util.spec_from_file_location(self._name, self._spec.origin)
            self._mods = importlib.util.module_from_spec(self._spec)
            self._mods.print = self.print
            self._mods.input = self.input
        
        self._prints = []
        self._inputs = []
        self._tests  = {}
        self._assert = {}
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