"""
The central unit test module.

This file supports a single function for running all the unit tests.  It is the 
primary test hook for __main__.py.  But __init__.py also exposes it in case you
do really want to run all tests and not just one test.

Author: Walker M. White (wmw2)
Date:   June 7, 2019
"""
# See: https://stackoverflow.com/questions/14132789/relative-imports-for-the-billionth-time
if __package__ is None or __package__ == '':
    # Access the module if run from __main__.py (Script visibility)
    import test_app
    import test_utils
    import test_pilots
    import test_violations
    import test_endorsements
    import test_inspections
else:
    # Access the module if run from __init__.py (Packages visibility)
    from . import test_app
    from . import test_utils
    from . import test_pilots
    from . import test_violations
    from . import test_endorsements
    from . import test_inspections


# Test the REQUIRE functionality (weather)
TEST_BASIC_APP   = 0
# Test the first extension (endorsements and certification)
TEST_EXTENSION_1 = 1
# Test the second extension (repairs)
TEST_EXTENSION_2 = 2


def test(level=TEST_BASIC_APP):
    """
    Tests all program features up to the given feature level.
    
    By default, it only checks the required functionality (weather minimums).
    A different value for level will include the test cases for the two
    extensions.
    
    Parameter level: The assignment level constant.
    Precondition: level is one of TEST_BASIC_APP,TEST_EXTENSION_1,TEST_EXTENSION_2
    """
    test_utils.test()
    test_pilots.test(level)
    test_violations.test()
    if level >= TEST_EXTENSION_1:
        test_endorsements.test()
    if level >= TEST_EXTENSION_2:
        test_inspections.test()
    test_app.test(level)
    print('The application passed all tests')
