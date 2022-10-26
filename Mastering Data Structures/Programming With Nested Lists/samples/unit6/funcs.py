"""
Mutable functions on a 2d list of numbers.

All of these functions are procedures.  They have no return values.

Author: Walker M. White
Date:   June 7, 2019
"""


def add_ones(table):
    """
    Adds one to every number in the table
    
    Example: If a= [[1,2],[3,4]]) then add_ones(a) changes a to [[2,3],[4,5]]
    
    Parameter table: The candidate table to modify
    Precondition: table is a rectangular 2d List of numbers
    """
    # Walk through table
    for rpos in range(len(table)):
        
        # Walk through each column
        for cpos in range(len(table[rpos])):
            table[rpos][cpos] = table[rpos][cpos]+1
    
    # No return statement


def strip(table,col):
    """
    Removes column col from the given table
    
    Example: If a= [[1,2,3],[4,5,6]]) then strip(a,1) changes a to [[1,3],[4,6]]
    
    Parameter table: The candidate table to modify
    Precondition: table is a rectangular 2d List of numbers
    
    Parameter col: The column to remove
    Precondition: col is an int and a valid column of table
    """
    # Walk through table
    for rpos in range(len(table)):
        
        # Modify each row to slice out column
        table[rpos] = table[rpos][:col] + table[rpos][col+1:]
    
    # No return statement

