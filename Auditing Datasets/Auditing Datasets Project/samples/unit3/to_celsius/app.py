"""
Module with the main "controlling" function.

THis module contains the function that decides what to do (test or run the application)
based on the command line arguments.

Why do we have this in its own file?  It is bad style to have any function definitions
in __main__.py.  That should only contain script code.  But because the application
can either convert (using temp.py) or test (using test.py), it does not make sense to
favor one over the other.  Therefore, we pulled this out into a separate file.

Author: Walker M. White (wmw2)
Date:   June 7, 2019
"""
import temp
import test

def execute(*args):
    """
    Executes the application or prints an error message if executed incorrectly.
    
    The arguments to the application (EXCLUDING the application name) are provided to
    the list args. This list should contain exactly one element: a number or the 
    string '--test'.  If it is '--test', it runs the test script.  Otherwise, it 
    converts the provided number to celsius.
    
    If the user calls this script incorrectly (either the wrong number of arguments,
    or passing something that is not a number), this function prints:
        
        Usage: python to_celsius number
    
    Parameter args: The command line arguments for the application (minus the application name)
    Precondition: args is a list of strings
    """
    # Quit if wrong number of arguments
    if len(args) != 1:
        print('Usage: python to_celsius number')
    elif args[0] == '--test':
        test.test_to_celsius()
    else:
        try:
            # Prepare to crash if user gives a non-number
            value = float(args[0])
            result = temp.to_celsius(value)
            print(result)
        except:
            print('Usage: python to_celsius number')
    