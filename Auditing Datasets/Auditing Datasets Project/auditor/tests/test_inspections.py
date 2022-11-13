# See: https://stackoverflow.com/questions/14132789/relative-imports-for-the-billionth-time
if __package__ is None or __package__ == '':
    # Access the module if run from __main__.py (Script visibility)
    from support import *
else:
    # Access the module if run from __init__.py (Packages visibility)
    from .support import *

# Load the utils module
utils = load_from_path('utils')
inspections = load_from_path('inspections')


def build_hours():
    """
    Returns a 2d list of plane hours by date (used for error messages).
    
    The date is in the format
        
        PLANE TIMEIN TIMEOUT HOURS
    
    Each entry can represent a flight, or a repair.  Normal repairs
    have a -1 for hours while annuals have a -2 for repairs.  Flights
    have the total hours flown for that flight.
    
    This data is sorted by timein, allowing us to quickly look-up 
    when producing error messages.
    """
    import datetime
    dataset = []
    
    parent = os.path.split(__file__)[0]
    fpath  = os.path.join(parent,'repairs.csv')
    for item in utils.read_csv(fpath)[1:]:
        start = utils.str_to_time(item[1])
        ends  = utils.str_to_time(item[2])
        type  = -2 if item[3] == 'annual inspection' else -1
        dataset.append([item[0],start,ends,type])
    
    fpath  = os.path.join(parent,'lessons.csv')
    for item in utils.read_csv(fpath)[1:]:
        start = utils.str_to_time(item[3]).replace(tzinfo=None)
        ends  = utils.str_to_time(item[4]).replace(tzinfo=None)
        hours = round((ends-start).seconds/(60*60))
        dataset.append([item[1],start,ends,hours])
    
    fpath  = os.path.join(parent,'fleet.csv')
    for item in utils.read_csv(fpath)[1:]:
        start = utils.str_to_time(item[5])
        end   = start+datetime.timedelta(seconds=1)
        hours = int(item[6])
        dataset.append([item[0],start,start,-2]) # Record annual    
        dataset.append([item[0],end,end,hours])  # Record carry over hours
    
    dataset.sort(key=lambda x:x[1])
    return dataset


def get_hours(plane,timestamp,hourset):
    """
    Returns the number of hours plane has flown BEFORE timestamp
    
    The number returned does not include the flight at timestamp (assuming
    it is a flight).
    
    Parameter plane: The id of a plane
    Precondition: plane is a string
    
    Parameter timestamp: The time to query
    Precondition: timestamp is a str representing a date in iso format
    
    Parameter hourset: The database of plane hours
    Precondition: hourset is 2d list created by build_hours()
    """
    date = utils.str_to_time(timestamp).replace(tzinfo=None)
    hours = 0
    pos = 0
    while pos < len(hourset):
        curr = hourset[pos]
        pos += 1
        if curr[0] == plane:
            if curr[1] < date:
                if curr[3] >= 0:
                    hours += curr[3]
                else:
                    hours = 0
            else:
                pos = len(hourset)
    return hours


def get_annual(plane,timestamp,hourset):
    """
    Returns the most recent annual for this plane BEFORE timestamp
    
    The value returned is actually (annual,days) where annual is date
    object (not a datetime object) and days is the number of days between
    timestamps and annual.
    
    Parameter plane: The id of a plane
    Precondition: plane is a string
    
    Parameter timestamp: The time to query
    Precondition: timestamp is a str representing a date in iso format
    
    Parameter hourset: The database of plane hours
    Precondition: hourset is 2d list created by build_hours()
    """
    date = utils.str_to_time(timestamp).replace(tzinfo=None)
    pos = 0
    annual = None
    while pos < len(hourset):
        curr = hourset[pos]
        pos += 1
        if curr[0] == plane and curr[3] == -2:
            if annual is None:
                annual = curr[1]
            elif curr[1] >= date:
                pos = len(hourset)
            elif annual < curr[1]:
                annual = curr[1]
    
    days = (date-annual).days
    return (annual.date(),days)


def get_repairs(plane,timestamp,hourset):
    """
    Returns the most recent repair for this plane that began BEFORE timestamp
    
    The value returned is actually (timein,timeout) where timein and timeout
    are both date objects (not a datetime objects).
    
    Parameter plane: The id of a plane
    Precondition: plane is a string
    
    Parameter timestamp: The time to query
    Precondition: timestamp is a str representing a date in iso format
    
    Parameter hourset: The database of plane hours
    Precondition: hourset is 2d list created by build_hours()
    """
    date = utils.str_to_time(timestamp).replace(tzinfo=None)
    pos = 0
    timein  = None
    timeout = None
    while pos < len(hourset):
        curr = hourset[pos]
        pos += 1
        if curr[0] == plane and curr[3] < 0:
            if timein is None:
                timein  = curr[1]
                timeout = curr[2]
            elif curr[1] >= date:
                pos = len(hourset)
            elif timein < curr[1]:
                timein  = curr[1]
                timeout = curr[2]
    
    return (timein.date(),timeout.date())


def false_negative(flight,hourset,reason=None):
    """
    Returns a message explaining a false negative result.
    
    Parameter flight: The flight that should have been detected
    Precondition: flight is a row in the correct list of answers
    
    Parameter hourset: The database of plane hours
    Precondition: hourset is 2d list created by build_hours()
    
    Parameter reason: The (incorrect) reason given (or None if missed)
    Precondition: reason is None or one of 'Inspection', 'Annual', 'Grounded', 'Maintenance'
    """
    message = None
    if reason == 'Maintenance' or flight[-1] == 'Maintenance':
        hours = get_hours(flight[1],flight[3],hourset)
        start = utils.str_to_time(flight[3]).replace(tzinfo=None)
        stop  = utils.str_to_time(flight[4]).replace(tzinfo=None)
        hours += (stop-start).seconds/(60*60)
        plural1 = 's' if hours != 1 else ''
        timein, timeout = get_repairs(flight[1],flight[3],hourset)
        annual, days = get_annual(flight[1],flight[3],hourset)
        plural2 = 's' if days != 1 else ''
        data = (flight[1],flight[4],hours,plural1,timeout.isoformat(),days,plural2,annual.isoformat())
        message = 'Plane %s landed on %s with %s hour%s since its last repair on %s and %s day%s since its last annual on %s.' % data
    elif flight[-1] == 'Inspection':
        hours = get_hours(flight[1],flight[3],hourset)
        start = utils.str_to_time(flight[3]).replace(tzinfo=None)
        stop  = utils.str_to_time(flight[4]).replace(tzinfo=None)
        hours += (stop-start).seconds/(60*60)
        plural = 's' if hours != 1 else ''
        data  = (flight[1],hours,plural,flight[3])
        message = 'Plane %s had %d hour%s after the flight at %s.' % data
    elif flight[-1] == 'Annual':
        annual, days = get_annual(flight[1],flight[3],hourset)
        plural = 's' if days != 1 else ''
        data = (flight[1],annual.isoformat(),repr(days),plural,flight[3])
        message = 'Plane %s last had an annual inspection on %s, %s day%s before %s.' % data
    elif flight[-1] == 'Grounded':
        timein, timeout = get_repairs(flight[1],flight[3],hourset)
        data = (flight[1],timein.isoformat(),timeout.isoformat(),flight[3])
        message = 'Plane %s was in maintenance between %s and %s, overlapping the flight at %s.' % data
    return message


def false_positive(flight,hourset):
    """
    Returns a message explaining a false positive result.
    
    Parameter flight: The flight that should have been detected
    Precondition: flight is a row in the correct list of answers
    
    Parameter hourset: The database of plane hours
    Precondition: hourset is 2d list created by build_hours()
    """
    message = None
    if flight[-1] == 'Inspection':
        hours = get_hours(flight[1],flight[3],hourset)
        start = utils.str_to_time(flight[3]).replace(tzinfo=None)
        stop  = utils.str_to_time(flight[4]).replace(tzinfo=None)
        hours += (stop-start).seconds/(60*60)
        explain = 'had exactly' if hours == 100 else 'only had'
        plural = 's' if hours != 1 else ''
        data  = (flight[1],explain,hours,plural,flight[3])
        message = 'Plane %s %s %d hour%s after the flight at %s.' % data
    elif flight[-1] == 'Annual':
        annual, days = get_annual(flight[1],flight[3],hourset)
        plural = 's' if days != 1 else ''
        data = (flight[1],annual.isoformat(),repr(days),plural,flight[3])
        message = 'Plane %s had an annual inspection on %s, %s day%s before %s.' % data
    elif flight[-1] == 'Grounded':
        timein, timeout = get_repairs(flight[1],flight[3],hourset)
        data = (flight[1],timeout.isoformat(),flight[3])
        message = 'Plane %s was last in maintenance on %s before the flight at %s.' % data
    else: # Maintenance
        hours = get_hours(flight[1],flight[3],hourset)
        start = utils.str_to_time(flight[3]).replace(tzinfo=None)
        stop  = utils.str_to_time(flight[4]).replace(tzinfo=None)
        hours += (stop-start).seconds/(60*60)
        plural1 = 's' if hours != 1 else ''
        timein, timeout = get_repairs(flight[1],flight[3],hourset)
        annual, days = get_annual(flight[1],flight[3],hourset)
        plural2 = 's' if days != 1 else ''
        data = (flight[1],flight[4],hours,plural1,timeout.isoformat(),days,plural2,annual.isoformat())
        message = 'Plane %s landed on %s with %s hour%s since its last repair on %s and %s day%s since its last annual on %s.' % data
    return message


def test_list_inspection_violations():
    """
    Tests the function list_inspection_violations
    """
    fcn = 'inspections.list_inspection_violations'
    
    parent = os.path.split(__file__)[0]
    results = inspections.list_inspection_violations(parent)
    
    fpath  = os.path.join(parent,'badplanes.csv')
    correct = utils.read_csv(fpath)[1:]
    
    # Lets construct a dataset for better feedback
    hourset = build_hours()
    
    # Hash for better comparison
    data = {}
    for item in results:
        if len(item) != len(correct[0]):
            quit_with_error('%s is not a (1-dimensional) list with %d elements.' % (item,len(correct[0])))
        data[item[0]+item[3]] = item
    results = data
    
    data = {}
    for item in correct:
        data[item[0]+item[3]] = item
    correct = data
    
    for key in correct:
        if not key in results:
            data = (fcn,correct[key][3],correct[key][0])
            message = '%s(tests) is missing the flight %s for pilot %s' % data
            message += '\n'+false_negative(correct[key],hourset)
            quit_with_error(message)
    
    for key in results:
        if not key in correct:
            data = (fcn,results[key][3],results[key][0])
            message = '%s(tests) identified flight %s for pilot %s, even though it is okay' % data
            message += '\n'+false_positive(results[key],hourset)
            quit_with_error(message)
    
    for key in correct:
        if correct[key][-1] != results[key][-1]:
            data = (fcn,correct[key][3],correct[key][0],repr(results[key][-1]),repr(correct[key][-1]))
            message = "%s('tests')  identified flight %s for pilot %s as %s, not %s" % data
            message += '\n'+false_negative(correct[key],hourset,results[key][-1])
            quit_with_error(message)
    
    print('  %s passed all tests' % fcn)


def test():
    """
    Performs all tests on the module endorsements.
    """
    print('Testing module inspections')
    test_list_inspection_violations()
