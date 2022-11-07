"""
Module showing the (primitive) way to convert types in a CSV files.

When reading a CSV file, all entries of the 2d list will be strings, even if you
originally entered them as numbers in Excel.  That is because CSV files (unlike
JSON) do not contain type information.

Author: Walker M. White
Date:   June 7, 2019
"""


def numify(table):
    """
    Modifies table so that all non-header rows contains numbers, not strings.

    The header row is assumed (as in all CSV files) to be names.  It will not
    be altered.

    Parameter table: The table to convert
    Precondition: table is a rectangular 2d list of strings.  Every row after
    the first contains strings that can all be converted to numbers.
    """

    # Altering, so must loop over positions
    for rpos in range(1,len(table)):           # Ignore the header
        # Loop over columns
        for cpos in range(len(table[rpos])):
            table[rpos][cpos] = float(table[rpos][cpos])
