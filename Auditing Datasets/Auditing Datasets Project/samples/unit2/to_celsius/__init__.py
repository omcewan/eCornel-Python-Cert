"""
Imports the to_centigrade function, renamed as "convert"

This file allows us to treat the to_celsius application as a module, so that we can
access the function(s) directly. Notice that this file only imports a single function,
and it renames it.  This is a common thing to do in __init__.py.  We have a bunch of
support functions to do the work, but we only expose the functions to the user that
we want to expose.

Author: Walker M. White (wmw2)
Date:   June 7, 2019
"""
# Note the period (.) before the temp.  This is what is known as a "relative" import
# Relative imports are what make __init__.py so hard. 
# See: https://stackoverflow.com/questions/14132789/relative-imports-for-the-billionth-time
from .temp import to_celsius as convert