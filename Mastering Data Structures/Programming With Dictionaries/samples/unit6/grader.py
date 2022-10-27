"""
Student grade example for dictionaries.

This module shows several a mutable function on dictionaries.

Author: Walker M. White
Date:   June 7, 2019
"""

# Global variable store the grade sheet
GRADES = {'jrs1':80,'jrs2':92,'wmw2':50,'abc1':95}


def give_extra_credit(grades,netids,bonus):
    """
    Gives bonus points to everyone in sequence netids
    
    This is a PROCEDURE.  It modifies the contents of grades. However, it only modifies 
    grades with a key that appears in the sequence netids.
    
    Parameter grades: The dictionary of student grades
    Precondition: grades has netids as keys, ints as values.
    
    Parameter netids: The list of students to give extra credit
    Precondition: netids is a list of valid (string) netids
    
    Parameter bonus: The extra credit bonus to award
    Precondition: bonus is an int
    """
    # No accumulator.  This is a procedure
    
    for student in netids:
        if student in grades:   # Test if student is a key in grades
            grades[student] = grades[student]+bonus
    


