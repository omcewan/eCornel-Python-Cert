"""
A module to demonstrate tracing of a try-except statement.

Look at the placement of the trace statements to see how to how to get debugging
information from a try-except statement.

Author: Walker M. White
Date: July 30, 2019
"""


def first(n):
    print('Start first')
    result = 0
    
    try:
        print('Start first try')
        result = second(n)
        print('End first try')
    except:
        print('In first except')
        result = -1
    
    print('Done first')
    return result


def second(n):
    print('Start second')
    result = 0
    
    try:
        print('Start second try')
        assert n <= 0, repr(n)+' is not <= 0'
        result = 2*n
        print('End second try')
    except:
        print('In second except')
        result = 2*n+1
    
    assert n >= 0, repr(n)+' is not >= 0'
    print('Done second')
    return result


# Have the student test
# first(-1)
# first(1)
# first(0)