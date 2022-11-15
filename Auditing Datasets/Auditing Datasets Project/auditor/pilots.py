"""
Module determining pilot certifications, ratings, and endorsements.

The restrictions that we place on a pilot depend on their qualifications.  There are three
ways to think about a pilot.  

(1) Certifications.  These are what licenses a pilot has.  We also use these to classify
where the student is in the licensing process.  Is the student post solo (can fly without
instructor), but before license?  Is the student 50 hours past their license (a threshold 
that helps with insurance)?

(2) Ratings.  These are extra add-ons that a pilot can add to a license. For this project,
the only rating is Instrument Rating, which allows a pilot to fly through adverse weather
using only instruments.

(3) Endorsements. These are permission to fly certain types of planes solo.  Advanced 
allows a pilot to fly a plane with retractable landing gear. Multiengine allows a pilot
to fly a plane with more than one engine.

The file pilots.csv is a list of all pilots in the school, together with the dates that
they earned these certifications, ratings, and endorsements.  Specifically, this CSV file
has the following header:
    
    ID  LASTNAME  FIRSTNAME  JOINED  SOLO  LICENSE  50 HOURS  INSTRUMENT  ADVANCED  MULTIENGINE

The first three columns are strings, while all other columns are dates.

The functions in this class take a row from the pilot table and determine if a pilot has
a certain qualification at the time of takeoff. As this program is auditing the school 
over a course of a year, a student may not be instrument rated for one flight but might
be for another.

The preconditions for many of these functions are quite messy.  While this makes writing 
the functions simpler (because the preconditions ensure we have less to worry about), 
enforcing these preconditions can be quite hard. That is why it is not necessary to 
enforce any of the preconditions in this module.

Author: Orlando McEwan
Date: 11/13/2022
"""
import utils


# CERTIFICATION CLASSIFICATIONS
# The certification of this pilot is unknown
PILOT_INVALID = -1
# A pilot that has joined the school, but has not soloed
PILOT_NOVICE = 0
# A pilot that has soloed but does not have a license
PILOT_STUDENT = 1
# A pilot that has a license, but has under 50 hours post license
PILOT_CERTIFIED = 2
# A pilot that 50 hours post license
PILOT_50_HOURS = 3


def get_certification(takeoff, student):
    """
    Returns the certification classification for this student at the time of takeoff.

    The certification is represented by an int, and must be the value PILOT_NOVICE, 
    PILOT_STUDENT, PILOT_CERTIFIED, PILOT_50_HOURS, or PILOT_INVALID. It is PILOT_50_HOURS 
    if the student has certified '50 Hours' before this flight takeoff.  It is 
    PILOT_CERTIFIED if the student has a private license before this takeoff and 
    PILOT_STUDENT if the student has soloed before this takeoff.  A pilot that has only
    just joined the school is PILOT_NOVICE.  If the flight takes place before the student
    has even joined the school, the result is PILOT_INVALID.

    Recall that a student is a 10-element list of strings.  The first three elements are
    the student's identifier, last name, and first name.  The remaining elements are all
    timestamps indicating the following in order: time joining the school, time of first 
    solo, time of private license, time of 50 hours certification, time of instrument 
    rating, time of advanced endorsement, and time of multiengine endorsement.

    Parameter takeoff: The takeoff time of this flight
    Precondition: takeoff is a datetime object with a time zone

    Parameter student: The student pilot
    Precondition: student is 10-element list of strings representing a pilot
    """
    # set the student as unknown cert status
    cert = PILOT_INVALID

    # loop through the student array but only from index 3 to 6 since they contain the values we need
    for idx in range(3, 7):

        # if at any point we dont get a value we just return the previous cert value.
        if len(student[idx]) < 1:
            return cert

        # get the datetime for the time stamp at that student index and set its time zone to the one of takeoff
        timestamp = utils.str_to_time(student[idx], takeoff)

        # compare the two datetime objects and either return or set their certs
        if takeoff.date() == timestamp.date():
            if idx == 3:
                return PILOT_NOVICE
            elif idx == 4:
                return PILOT_STUDENT
            elif idx == 5:
                return PILOT_CERTIFIED
            elif idx == 6:
                return PILOT_50_HOURS

        elif timestamp.date() < takeoff.date():
            if idx == 3:
                cert = PILOT_NOVICE
            elif idx == 4:
                cert = PILOT_STUDENT
            elif idx == 5:
                cert = PILOT_CERTIFIED
            elif idx == 6:
                cert = PILOT_50_HOURS
    return cert


def has_instrument_rating(takeoff, student):
    """
    (OPTIONAL)
    Returns True if the student has an instrument rating at the time of takeoff, False otherwise

    Recall that a student is a 10-element list of strings.  The first three elements are
    the student's identifier, last name, and first name.  The remaining elements are all
    timestamps indicating the following in order: time joining the school, time of first 
    solo, time of private license, time of 50 hours certification, time of instrument 
    rating, time of advanced endorsement, and time of multiengine endorsement.

    NOTE: Just because a pilot has an instrument rating does not mean that every flight
    with that pilot is an IFR flight.  It just means the pilot could choose to use VFR
    or IFR rules.

    Parameter takeoff: The takeoff time of this flight
    Precondition: takeoff is a datetime object

    Parameter student: The student pilot
    Precondition: student is 10-element list of strings representing a pilot
    """
    if len(student[7]) < 1:
        return False

    instrument_time = utils.str_to_time(student[7], takeoff)
    if instrument_time <= takeoff:
        return True
    else:
        return False


def has_advanced_endorsement(takeoff, student):
    """
    (OPTIONAL)
    Returns True if the student has an endorsement to fly an advanced plane at the time of takeoff.

    The function returns False otherwise.

    Recall that a student is a 10-element list of strings.  The first three elements are
    the student's identifier, last name, and first name.  The remaining elements are all
    timestamps indicating the following in order: time joining the school, time of first 
    solo, time of private license, time of 50 hours certification, time of instrument 
    rating, time of advanced endorsement, and time of multiengine endorsement.

    Parameter takeoff: The takeoff time of this flight
    Precondition: takeoff is a datetime object

    Parameter student: The student pilot
    Precondition: student is 10-element list of strings representing a pilot
    """
    if len(student[8]) < 1:
        return False

    endorsment_time = utils.str_to_time(student[8], takeoff)
    if endorsment_time <= takeoff:
        return True
    else:
        return False


def has_multiengine_endorsement(takeoff, student):
    """
    (OPTIONAL)
    Returns True if the student has an endorsement to fly an multiengine plane at the time of takeoff.

    The function returns False otherwise.

    Recall that a student is a 10-element list of strings.  The first three elements are
    the student's identifier, last name, and first name.  The remaining elements are all
    timestamps indicating the following in order: time joining the school, time of first 
    solo, time of private license, time of 50 hours certification, time of instrument 
    rating, time of advanced endorsement, and time of multiengine endorsement.

    Parameter takeoff: The takeoff time of this flight
    Precondition: takeoff is a datetime object

    Parameter student: The student pilot
    Precondition: student is 10-element list of strings representing a pilot
    """
    if len(student[9]) < 1:
        return False

    endorsment_time = utils.str_to_time(student[9], takeoff)
    if endorsment_time <= takeoff:
        return True
    else:
        return False


def get_best_value(data, index, maximum=True):
    """
    Returns the 'best' value from a given column in a 2-dimensional nested list.

    This function is a helper function for get_minimums (whose docstring you should
    read and understand first). 

    The data parameter is a 2-dimensional nested list of data.  The index parameter
    indicates which "colummn" of data should be evaluated. Each item in that column
    is expected to be a number in string format.  Each item should be evaluated as a 
    float and the best value selected as the return value for the function. The
    best value is determined by the maximum parameter and is either the highest or
    lowest float value.

    The 2D list does not include a header row. It should not be modified in any way.

    Parameter data: a 2-dimensional nested list of data
    Precondition: the column referenced by index should by numbers in string format

    Parameter index: position to examine in each row of data
    Precondition: index is a an integer

    Parameter maximum: indicates whether to return the highest value (True) or
    lowest value (False)
    Precondition: maximum is a boolean and defaults to True

    """
    # Find the best values for each column of the row
    rows = len(data)

    # set best_value as the index value of the first row
    best_value = float(data[0][index])

    if maximum == True:
        for row in range(1, rows):
            if float(data[row][index]) > best_value:
                best_value = float(data[row][index])
    else:
        for row in range(1, rows):
            if float(data[row][index]) < best_value:
                best_value = float(data[row][index])

    return float(best_value)


def get_minimums(cert, area, instructed, vfr, daytime, minimums):
    """
    Returns the most advantageous minimums for the given flight category.

    The minimums is the 2-dimensional list (table) of minimums, including the header.
    The header for this table is as follows:

        CATEGORY  CONDITIONS  AREA  TIME  CEILING  VISIBILITY  WIND  CROSSWIND

    The values in the first four columns are strings, while the values in the last
    four columns are numbers.  CEILING is a measurement in ft, while VISIBILITY is in
    miles.  Both WIND and CROSSWIND are speeds in knots.

    This function first searches the table for rows that match the function parameters. 
    It is possible for more than one row to be a match.  A row is a match if ALL four 
    of the first four columns match.

    The first column (CATEGORY) has values 'Student', 'Certified', '50 Hours', or 'Dual'.
    If the value 'Student', it is a match if cert is PILOT_STUDENT or higher.  If the
    value is 'Certified', it is a match if cert is PILOT_CERTIFIED or higher. If it is 
    '50 Hours', it is only a match if cert is PILOT_50_HOURS. The value 'Dual' only
    matches if instructed is True and even if cert is PILOT_INVALID or PILOT_NOVICE.

    The second column (CONDITIONS) has values 'VMC' and 'IMC'. A flight filed as VFR 
    (visual flight rules) is subject to VMC (visual meteorological conditions) minimums.  
    Similarly, a fight filed as IFR is subject to IMC minimums.

    The third column (AREA) has values 'Pattern', 'Practice Area', 'Local', 
    'Cross Country', or 'Any'. Flights that are in the pattern or practice area match
    'Local' as well.  All flights match 'Any'.

    The fourth column (TIME) has values 'Day' or 'Night'. The value 'Day' is only 
    a match if daytime is True. If it is False, 'Night' is the only match.

    Once the function finds the all matching rows, it searches for the most advantageous
    values for CEILING, VISIBILITY, WIND, and CROSSWIND. Lower values of CEILING and
    VISIBILITY are better.  Higher values for WIND and CROSSWIND are better.  It then
    returns this four values as a list of four floats (in the same order they appear)
    in the table.

    Example: Suppose minimums is the table

        CATEGORY   CONDITIONS  AREA           TIME  CEILING  VISIBILITY  WIND  CROSSWIND
        Student    VMC         Pattern        Day   2000     5           20    8
        Student    VMC         Practice Area  Day   3000     10          20    8
        Certified  VMC         Local          Day   3000     5           20    20
        Certified  VMC         Practice Area  Night 3000     10          20    10
        50 Hours   VMC         Local          Day   3000     10          20    10
        Dual       VMC         Any            Day   2000     10          30    10
        Dual       IMC         Any            Day   500      0.75        30    20

    The call get_minimums(PILOT_CERTIFIED,'Practice Area',True,True,True,minimums) matches
    all of the following rows:

        Student    VMC         Practice Area  Day   3000     10          20    8
        Certified  VMC         Local          Day   3000     5           20    20
        Dual       VMC         Any            Day   2000     10          30    10

    The answer in this case is [2000,5,30,20]. 2000 and 5 are the least CEILING and 
    VISIBILITY values while 30 and 20 are the largest wind values.

    If there are no rows that match the parameters (e.g. a novice pilot with no 
    instructor), this function returns None.

    Parameter cert: The pilot certification
    Precondition: cert is an int and one of PILOT_NOVICE, PILOT_STUDENT, PILOT_CERTIFIED, 
    PILOT_50_HOURS, or PILOT_INVALID.

    Parameter area: The flight area for this flight plan
    Precondition: area is a string and one of 'Pattern', 'Practice Area' or 'Cross Country'

    Parameter instructed: Whether an instructor is present
    Precondition: instructed is a boolean

    Parameter vfr: Whether the pilot has filed this as an VFR flight
    Precondition: vfr is a boolean

    Parameter daytime: Whether this flight is during the day
    Precondition: daytime is boolean

    Parameter minimums: The table of allowed minimums
    Precondition: minimums is a 2d-list (table) as described above, including header
    """
    # Find all rows that can apply to this student
    # Find the best values for each column of the row
    # HINT: remember to use get_best_value to find best value in list of matches

    # get the number of rows in the 2d list, we will use this to set the range for our loop
    rows = len(minimums)

    # keeps track of all the rows that match the criteria
    matching_rows = []

    # start from row 1 since the first row, row 0, is just the headers
    for row in range(1, rows):

        # this will keep boolean values for each col value, if all the values of match are true then its a match and we append to matching_rows
        match = []

        # we are only checking the values in the first four columns so we only need from index 0 - 3.
        for col in range(0, 4):
            if minimums[0][col] == "CATEGORY":
                if minimums[row][col] == "Student":
                    if cert >= PILOT_STUDENT:
                        match.append("CATERGORY")
                elif minimums[row][col] == "Certified":
                    if cert >= PILOT_CERTIFIED:
                        match.append("CATERGORY")
                elif minimums[row][col] == "50 Hours":
                    if cert == PILOT_50_HOURS:
                        match.append("CATERGORY")
                elif minimums[row][col] == "Dual" and instructed == True:
                    match.append("CATERGORY")
            elif minimums[0][col] == "CONDITIONS":
                if minimums[row][col] == "VMC":
                    if vfr == True:
                        match.append("CONDITIONS")
                elif minimums[row][col] == "IMC":
                    if vfr == False:
                        match.append("CONDITIONS")
            elif minimums[0][col] == "AREA":
                if area == "Pattern":
                    if minimums[row][col] == "Pattern" or minimums[row][col] == "Local" or minimums[row][col] == "Any":
                        match.append("AREA")
                elif area == 'Practice Area':
                    if minimums[row][col] == "Practice Area" or minimums[row][col] == "Local" or minimums[row][col] == "Any":
                        match.append('AREA')
                elif area == 'Cross Country':
                    if minimums[row][col] == "Cross Country" or minimums[row][col] == "Any":
                        match.append('AREA')
            elif minimums[0][col] == "TIME":
                if minimums[row][col] == "Day":
                    if daytime == True:
                        match.append("TIME")
                elif minimums[row][col] == "Night":
                    if daytime == False:
                        match.append("TIME")
        if len(match) == 4:
            matching_rows.append(minimums[row][4:])

    if len(matching_rows) < 1:
        return

    best_values = [get_best_value(matching_rows, 0, False),
                   get_best_value(matching_rows, 1, False),
                   get_best_value(matching_rows, 2, True),
                   get_best_value(matching_rows, 3, True),
                   ]

    # this loop will find a row that matches the best values array we loop through each row in the matching rows 2d array
    for row in range(len(matching_rows)):
        # here we loop through the columns of each of the row and check if that col value in best values
        for col in range(len(matching_rows[0])):
            if best_values[col] == float(matching_rows[row][col]):
                # this checks if we have gone through each element and we are at the last element of the row and if we are we return cause that means all the values match and we have a match in the data
                if col == len(matching_rows[0]) - 1:
                    return best_values
            else:
                break
    return
