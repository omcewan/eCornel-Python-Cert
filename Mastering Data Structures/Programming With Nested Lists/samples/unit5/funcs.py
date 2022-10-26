"""
Immutable (accumulator) functions on a 2d list of numbers.

This version of the module shows off completed functions.

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
    result = True
    
    # Walk through table
    for row in table:
    
        # Walk through the row
        for item in row:
            if not type(item) in [int,float]:
                result = False
    
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
    # Find the size of the (non-ragged) table
    numrows = len(table)
    numcols = len(table[0]) # All rows have same no. cols
    
    # Build the table
    result = [] # Result accumulator
    for m in range(numcols):
        
        # Make a single row
        row = [] # Single row accumulator
        for n in range(numrows):
            row.append(table[n][m])
        
        #Add the result to the table
        result.append(row)
    
    return result
