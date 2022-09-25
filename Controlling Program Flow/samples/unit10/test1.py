"""
Test script for the module anglicize

Author: Walker M. White
Date:   March 30, 2019
"""
import introcs              # testing functions
import funcs                # functions to be tested


def test_anglicize():
    """
    Test procedure for the primary anglicize function
    """
    print('Testing anglicize')
    result = funcs.anglicize(1)
    introcs.assert_equals("one", result)

    result = funcs.anglicize(19)
    introcs.assert_equals("nineteen", result)

    result = funcs.anglicize(20)
    introcs.assert_equals("twenty", result)

    result = funcs.anglicize(35)
    introcs.assert_equals("thirty five", result)

    result = funcs.anglicize(50)
    introcs.assert_equals("fifty", result)

    result = funcs.anglicize(99)
    introcs.assert_equals("ninety nine", result)

    result = funcs.anglicize(100)
    introcs.assert_equals("one hundred", result)

    result = funcs.anglicize(301)
    introcs.assert_equals("three hundred one", result)

    result = funcs.anglicize(999)
    introcs.assert_equals("nine hundred ninety nine", result)

    result = funcs.anglicize(1000)
    introcs.assert_equals("one thousand", result)

    result = funcs.anglicize(1009)
    introcs.assert_equals("one thousand nine", result)

    result = funcs.anglicize(900000)
    introcs.assert_equals("nine hundred thousand", result)

    result = funcs.anglicize(789436)
    introcs.assert_equals("seven hundred eighty nine thousand four hundred thirty six",
                              result)


def test_anglicize1000():
    """
    Test procedure for the helper function anglicize1000
    """
    print('Testing anglicize1000')

    result = funcs.anglicize1000(1)
    introcs.assert_equals("one", result)

    result = funcs.anglicize1000(19)
    introcs.assert_equals("nineteen", result)

    result = funcs.anglicize1000(20)
    introcs.assert_equals("twenty", result)

    result = funcs.anglicize1000(35)
    introcs.assert_equals("thirty five", result)

    result = funcs.anglicize1000(50)
    introcs.assert_equals("fifty", result)

    result = funcs.anglicize1000(99)
    introcs.assert_equals("ninety nine", result)

    result = funcs.anglicize1000(100)
    introcs.assert_equals("one hundred", result)

    result = funcs.anglicize1000(301)
    introcs.assert_equals("three hundred one", result)

    result = funcs.anglicize1000(999)
    introcs.assert_equals("nine hundred ninety nine", result)


def test_anglicize100to999():
    """
    Test procedure for the helper function anglicize100to999
    """
    print('Testing anglicize100to999')

    result = funcs.anglicize100to999(100)
    introcs.assert_equals("one hundred", result)

    result = funcs.anglicize100to999(301)
    introcs.assert_equals("three hundred one", result)

    result = funcs.anglicize100to999(999)
    introcs.assert_equals("nine hundred ninety nine", result)


def test_anglicize20to99():
    """
    Test procedure for the helper function anglicize20to99
    """
    print('Testing anglicize20to99')

    result = funcs.anglicize20to99(35)
    introcs.assert_equals("thirty five", result)

    result = funcs.anglicize20to99(50)
    introcs.assert_equals("fifty", result)

    result = funcs.anglicize20to99(99)
    introcs.assert_equals("ninety nine", result)


def test_anglicize1to19():
    """
    Test procedure for the helper function anglicize1to19
    """
    print('Testing anglicize1to19')

    result = funcs.anglicize1to19(1)
    introcs.assert_equals("one", result)

    result = funcs.anglicize1to19(2)
    introcs.assert_equals("two", result)

    result = funcs.anglicize1to19(3)
    introcs.assert_equals("three", result)

    result = funcs.anglicize1to19(4)
    introcs.assert_equals("four", result)

    result = funcs.anglicize1to19(5)
    introcs.assert_equals("five", result)

    result = funcs.anglicize1to19(6)
    introcs.assert_equals("six", result)

    result = funcs.anglicize1to19(7)
    introcs.assert_equals("seven", result)

    result = funcs.anglicize1to19(8)
    introcs.assert_equals("eight", result)

    result = funcs.anglicize1to19(9)
    introcs.assert_equals("nine", result)

    result = funcs.anglicize1to19(10)
    introcs.assert_equals("ten", result)

    result = funcs.anglicize1to19(11)
    introcs.assert_equals("eleven", result)

    result = funcs.anglicize1to19(12)
    introcs.assert_equals("twelve", result)

    result = funcs.anglicize1to19(13)
    introcs.assert_equals("thirteen", result)

    result = funcs.anglicize1to19(14)
    introcs.assert_equals("fourteen", result)

    result = funcs.anglicize1to19(15)
    introcs.assert_equals("fifteen", result)

    result = funcs.anglicize1to19(16)
    introcs.assert_equals("sixteen", result)

    result = funcs.anglicize1to19(17)
    introcs.assert_equals("seventeen", result)

    result = funcs.anglicize1to19(18)
    introcs.assert_equals("eighteen", result)

    result = funcs.anglicize1to19(19)
    introcs.assert_equals("nineteen", result)


def test_tens():
    """
    Test procedure for the helper function tens
    """
    print('Testing tens')
    result = funcs.tens(2)
    introcs.assert_equals("twenty", result)

    result = funcs.tens(3)
    introcs.assert_equals("thirty", result)

    result = funcs.tens(4)
    introcs.assert_equals("forty", result)

    result = funcs.tens(5)
    introcs.assert_equals("fifty", result)

    result = funcs.tens(6)
    introcs.assert_equals("sixty", result)

    result = funcs.tens(7)
    introcs.assert_equals("seventy", result)

    result = funcs.tens(8)
    introcs.assert_equals("eighty", result)

    result = funcs.tens(9)
    introcs.assert_equals("ninety", result)


# Script code.  This is run even on import.
test_tens()
test_anglicize1to19()
test_anglicize20to99()
test_anglicize100to999()
test_anglicize1000()
test_anglicize()
print('Module anglicize is working correctly')
