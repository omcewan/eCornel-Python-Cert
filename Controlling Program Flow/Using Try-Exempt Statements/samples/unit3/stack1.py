"""
A module to show off hwo to recover from an error.

This module shows what happens when there is not a try-except statement
immediately around the error, but there is one up higher in the call stack.

Author: Walker M. White
Date:   March 30, 2019
"""


def function_1(x,y):
    """
    Have function_2 do all the work
    """
    print('Starting function_1')
    result = 0 # try-except is like if-else.  Initialize a var for right scope
    try:
        print('Starting try')
        result = function_2(x,y)
        print('Completing try')
    except:
        print('Starting except')
        result = float('inf')
        print('Completing except')
    print('Completing function_1')
    return result


def function_2(x,y):
    """
    Have function_3 do all the work
    """
    print('Starting function_2')
    result = function_3(x,y)
    print('Completing function_2')
    return result


def function_3(x,y):
    """Returns: x divided by y"""
    print('Starting function_3')
    result = x/y
    print('Completing function_3')
    return result


# Script Code
if __name__ == "__main__":
    print(function_1(1,0))
