"""
Application code to convert farenheit to celsius.

This application uses the command line arguments to determine what to do (test the 
application or convert).  Since __main__.py should be limited to script code, this
file just passes the command line arguments to the module app.py which does all the
work.

Author: Walker M. White (wmw2)
Date:   June 7, 2019
"""
import app
import sys

# Remove the application name
arguments = sys.argv[1:]
app.execute(*arguments)
