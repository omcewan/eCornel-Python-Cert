"""
The top level module for the unit test script

This file is provided so that you can import the test module instead of running
it as a script. This allows you to isolate the tests, running one at a time 
instead of running all tests all the time.

Author: Walker M. White (wmw2)
Date:   June 7, 2019
"""
from .test_all import test as test_all
from .test_app import test as test_app
from .test_utils import test as test_utils
from .test_pilots import test as test_pilots
from .test_violations import test as test_violations
from .test_endorsements import test as test_endorsements
from .test_inspections import test as test_inspections
from .test_app import TEST_BASIC_APP, TEST_EXTENSION_1, TEST_EXTENSION_2
