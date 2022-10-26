"""
Immutable (accumulator) functions on a 2d list of numbers.

This version of the module shows off the stubs (before the functions are completed).

Author: Walker M. White
Date:   June 7, 2019
"""


def all_nums(table):
    """
    Returns True if table contains only numbers (False otherwise)
    
    Example: all_nums([[1,2],[3,4]]) is True
    all_nums([[1,2],[3,'a']]) is False
    
    Parameter table: The candidate table to modify
    Preconditions: table is a rectangular 2d List
    """
    result = True # Accumulator
    
    # Check each row
        # Check each item in each row
    
    return result


def transpose(table):
    """
    Returns a copy of table with rows and columns swapped
    
    Example:
           1  2          1  3  5
           3  4    =>    2  4  6
           5  6
    
    Parameter table: the table to transpose
    Precondition: table is a rectangular 2d List of numbers
    """
    result = []                       # Result (new table) accumulator 
    
    # Loop over columns
        # Add each column as a row to result
    
    return result


def transpose(table):
    """
    Returns a copy of table with rows and columns swapped
    
    Example:
           1  2          1  3  5
           3  4    =>    2  4  6
           5  6
    
    Parameter table: the table to transpose
    Precondition: table is a rectangular 2d List of numbers
    """
    numrows = len(table)     # Need number of rows
    numcols  = len(table[0]) # All rows have same no. cols
    
    result = []                       # Result (new table) accumulator 
    
    for m in range(numcols):
        # Get the column elements at position m
        # Make a new list for this column
        # Add this row to accumulator table
    
    return result
