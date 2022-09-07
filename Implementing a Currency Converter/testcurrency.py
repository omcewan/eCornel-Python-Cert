"""
Unit tests for module currency

When run as a script, this module invokes several procedures that test
the various functions in the module currency.

Author: Orlando McEwan
Date:   09/02/2022
"""

import introcs

import currency

def test_before_space():
    """
    Test procedure for before_space
    """
    print('Testing before_space')
    
    result = currency.before_space("Hello World")
    introcs.assert_equals("Hello",result)
    
    result = currency.before_space(" Hello World")
    introcs.assert_equals("",result)
    
    result = currency.before_space("Hello  World")
    introcs.assert_equals("Hello",result)
    
    result = currency.before_space(" Hello")
    introcs.assert_equals("",result)
    

def test_after_space():
    """
    Test procedure for after_space
    """
    print("Testing after_space")
    
    result = currency.after_space("Hello World")
    introcs.assert_equals("World",result)
    
    result = currency.after_space(" Hello World")
    introcs.assert_equals("Hello World",result)
    
    result = currency.after_space("Hello  World")
    introcs.assert_equals(" World",result)
    
    result = currency.after_space("Hello ")
    introcs.assert_equals("",result)


def test_first_inside_quotes():
    """
    Test procedure for first_inside_quotes
    """
    print("Testing first_inside_quotes")
    
    result = currency.first_inside_quotes("He\"ll\"o")
    introcs.assert_equals("ll", result)
    
    result = currency.first_inside_quotes("H\"e\"ll\"o")
    introcs.assert_equals("e", result)
    
    result = currency.first_inside_quotes('"Hello"')
    introcs.assert_equals("Hello", result)
    
    result = currency.first_inside_quotes('""Hello')
    introcs.assert_equals("", result)
    
    


def test_get_src():
    """
    Test procedure for get_src
    """
    print("Testing get_src")
    
    result = currency.get_src('{"success": true, "src": "2 United States Dollars", "dst": "1.772814 Euros", "error": ""}')
    introcs.assert_equals('2 United States Dollars', result)
    
    result = currency.get_src('{"success":false,"src":"","dst":"","error":"Source currency code is invalid."}')
    introcs.assert_equals('', result)
    
    result = currency.get_src('{"success": true, "src":"2 United States Dollars", "dst": "1.772814 Euros", "error": ""}')
    introcs.assert_equals('2 United States Dollars', result)
    
    result = currency.get_src('{"success":false,"src": "","dst":"","error":"Source currency code is invalid."}')
    introcs.assert_equals('', result)

def test_get_dst():
    """
    Test procedure for get_dst
    """
    print("Testing get_dst")


def test_has_error():
    """
    Test procedure for has_error
    """
    print("Testing has_error")


def test_service_response():
    """
    Test procedure for service_response
    """
    print("Testing service_response")


def test_iscurrency():
    """
    Test procedure for iscurrency
    """
    print("Testing iscurrency")


def test_exchange():
    """
    Test procedure for exchange
    """
    print("Testing exchange")


test_before_space()
test_after_space()
test_first_inside_quotes()
test_get_src()
# test_get_dst()
# test_has_error()
# test_service_response()
# test_iscurrency()
# test_exchange()
print("All tests completed successfully")
