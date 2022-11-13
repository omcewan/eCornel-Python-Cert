"""
Module to check inspection violations for a flight lesson (OPTIONAL)

There are three kinds of inspection violations. (1) A plane has gone more than
a year since its annual inspection. (2) A plane has accrued 100 hours of flight
time since its last regular inspection. (3) A plane is used for a lesson despite
the repair logs claiming that it is in the shop for maintenance.

This module is MUCH more difficult than the others.  In the other modules, we
provided specifications for all of the helper functions, to make the main
function (listing all violations) easier.  We do not do that at all here.
You have one specification for one function.  Any additional functions (which
we do recommend) are up to you.

The other tricky part is keeping track of the hours since the last inspection
for each plane.  It is possible to do this with a nested loop, but the result
will be very slow (the application will take several minutes to complete).
To speed it up, you have to figure out how to "interleave" lessons with repairs.
This is a very advanced programming problem.

To implement this module, you need to familiarize yourself with two files
beyond what you have used already.

First of all, recall that fleet.csv is a CSV file with the following header:

    TAILNO  TYPE  CAPABILITY  ADVANCED  MULTIENGINE ANNUAL  HOURS

This lists the planes at the flight school.  For this module you need the
last two columns, which are strings representing a date and an number,
respectively.  The date is the last annual inspection for that plane as of
the beginning of the year (e.g. the start of the audit).  The number is
the number of hours since the last 100 hour inspection.

In addition, repairs.csv is a CSV file with the following header:

    TAILNO  IN-DATE  OUT-DATE  DESCRIPTION

The first column is the string identifying the plane.  The next two columns are
strings representing dates, for when the plane enters and leaves the shop (so
it should not fly during this time).  The last column is the type of repair.
A plane must be inspected/repaired every 100 hours.  In addition, it must have
an annual inspection once a year.  Other repairs happen as needed.  ANY repair
resets the number of hours on the plane.

The preconditions for many of these functions are quite messy.  While this
makes writing the functions simpler (because the preconditions ensure we have
less to worry about), enforcing these preconditions can be quite hard. That is
why it is not necessary to enforce any of the preconditions in this module.

Author: YOUR NAME HERE
Date: THE DATE HERE
"""
import os.path
import datetime
import utils

# FILENAMES
# Sunrise and sunset (mainly useful for timezones, since repairs do not have them)
DAYCYCLE = 'daycycle.json'
# The list of all take-offs (and landings)
LESSONS  = 'lessons.csv'
# The list of all planes in the flight school
PLANES   = 'fleet.csv'
# The list of all repairs made to planes over the past year
REPAIRS  = 'repairs.csv'


def list_inspection_violations(directory):
    """
    Returns the (annotated) list of flight lessons that violate inspection
    or repair requirements.
    
    This function reads the data files in the given directory (the data files
    are all identified by the constants defined above in this module).  It loops
    through the list of flight lessons (in lessons.csv), identifying those
    takeoffs for which (1) a plane has gone MORE than a year since its annual
    inspection, (2) a plane has accrued OVER 100 hours of flight time since its
    last repair or inspection, and (3) a plane is used for a lesson despite
    the repair logs claiming that it is in the shop for maintenance.
    
    Note that a plane landing with exactly 100 hours used is not a violation.
    Nor is a plane that has flown with 365 days since its last inspection. This
    school likes to cut things close to safe money, but these are technically
    not violations.
    
    This function returns a list that contains a copy of each violating lesson,
    together with the violation appended to the lesson.  Violation of type (1)
    is annotated 'Annual'.  Violation of type (2) is annotated 'Inspection'.
    Violations of type (3) is annotated 'Grounded'.  If more than one is
    violated, it should be annotated 'Maintenance'.
    
    Example: Suppose that the lessons
    
        S00898  811AX  I072  2017-01-27T13:00:00-05:00  2017-01-27T15:00:00-05:00  VFR  Pattern
        S00681  684TM  I072  2017-02-26T14:00:00-05:00  2017-02-26T17:00:00-05:00  VFR  Practice Area
        S01031  738GG  I010  2017-03-19T13:00:00-04:00  2017-03-19T15:00:00-04:00  VFR  Pattern
    
    violate for reasons of 'Annual', 'Inspection', and 'Grounded', respectively
    (and are the only violations).  Then this function will return the 2d list
    
        [['S00898', '811AX', 'I072', '2017-01-27T13:00:00-05:00', '2017-01-27T15:00:00-05:00', 'VFR', 'Pattern', 'Annual'],
         ['S00681', '684TM', 'I072', '2017-02-26T14:00:00-05:00', '2017-02-26T17:00:00-05:00', 'VFR', 'Practice Area', 'Inspection'],
         ['S01031', '738GG', 'I010', '2017-03-19T13:00:00-04:00', '2017-03-19T15:00:00-04:00', 'VFR', 'Pattern', 'Grounded']]
    
    Parameter directory: The directory of files to audit
    Precondition: directory is the name of a directory containing the files
    'daycycle.json', 'fleet.csv', 'repairs.csv' and 'lessons.csv'
    """
    # You are on your own
    pass
