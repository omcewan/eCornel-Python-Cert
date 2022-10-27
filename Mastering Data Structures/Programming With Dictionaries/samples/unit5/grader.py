"""
Student grade examples for dictionaries.

This module shows several immutable functions on dictionaries.

Author: Walker M. White
Date:   June 7, 2019
"""

# Global variable store the grade sheet
GRADES = {'jrs1':80,'jrs2':92,'wmw2':50,'abc1':95}


def max_grade(grades):
    """
    Returns the maximum grade in the grade dictionary
    
    Parameter grades: The dictionary of student grades
    Precondition: grades has netids as keys, ints as values
    """
    maximum = 0
    
    # Loop over keys
    for k in grades:
        if grades[k] > maximum:
            maximum = grades[k]
    
    return maximum


def netids_above_cutoff(grades,cutoff):
    """
    Returns the list of netids with grades above or equal to cutoff
    
    Parameter grades: The dictionary of student grades
    Precondition: grades has netids as keys, ints as values.
    
    Parameter cutoff: The grade cutoff (for, say, a passing grade)
    Precondition: cutoff is an int
    """
    result = []                 # Accumulator
    
    for k in grades:
        if grades[k] >= cutoff:
            result.append(k)    # Add k to the list result
    
    return result