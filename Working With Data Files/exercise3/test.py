"""  
A completed test script for the time functions.

Notice how complicated testing is now.  To test that the return value of a function is
correct, we need to test (1) its type and (2) each attribute separately.  Because 
functions can now modify the arguments, we also need to verify that arguments are not
modified unless the specification specifically says they are.

Author: Walker M. White
Date: August 9, 2019
"""
import func
import introcs
import os.path

# The proper contents for file1.csv
FILE1 = [['STUDENT','AIRPLANE','INSTRUCTOR','TAKEOFF','LANDING','FILED','AREA'],
['S00309','738GG','I076','2015-01-12T09:00:00-05:00','2015-01-12T11:00:00-05:00','VFR','Pattern'],
['S00308','133CZ','I053','2015-01-13T09:00:00-05:00','2015-01-13T12:00:00-05:00','VFR','Practice Area'],
['S00324','426JQ','I053','2015-02-04T11:00:00-05:00','2015-02-04T14:00:00-05:00','VFR','Cross Country'],
['S00319','811AX','I072','2015-02-06T13:00:00-05:00','2015-02-06T15:00:00-05:00','VFR','Pattern'],
['S00321','738GG','I072','2015-02-08T10:00:00-05:00','2015-02-08T13:00:00-05:00','VFR','Practice Area'],
['S00308','811AX','I072','2015-02-23T09:00:00-05:00','2015-02-23T13:00:00-05:00','VFR','Cross Country']]


# The proper contents for file2.csv
FILE2 = [['TAIL NO','TYPE','CAPABILITY','ADVANCED','MULTIENGINE','ANNUAL','HOURS'],
['133CZ','Cessna 152','VFR','No','No','2016-04-15','88'],
['811AX','Cessna 152','VFR','No','No','2016-01-22','39'],
['426JQ','Cessna 152','VFR','No','No','2016-07-30','31']]


def test_write_csv():
    """
    Test procedure for the function write_csv()
    """
    print('Testing write_csv()')
    
    # Access the file relative to this one, not the user's terminal
    parent = os.path.split(__file__)[0]
    
    # First test (erase any existing file)
    fpath  = os.path.join(parent,'files','temp1.csv')
    open(fpath,'w').close()
    func.write_csv(FILE1,fpath)
    
    # Check file was created
    introcs.assert_true(os.path.exists(fpath))
    
    file = open(fpath)
    actual  =  file.read()
    file.close()
    
    file = open(os.path.join(parent,'files','writecsv1.csv'))
    correct = file.read()
    file.close()
    
    # Check to see if they are the same
    introcs.assert_equals(correct,actual)
    
    # Second test (erase any existing file)
    fpath  = os.path.join(parent,'files','temp2.csv')
    open(fpath,'w').close()
    func.write_csv(FILE2,fpath)
    
    # Check file was created
    introcs.assert_true(os.path.exists(fpath))
    
    file = open(fpath)
    actual  =  file.read()
    file.close()
    
    file = open(os.path.join(parent,'files','writecsv2.csv'))
    correct = file.read()
    file.close()
    
    # Check to see if they are the same
    introcs.assert_equals(correct,actual)


if __name__ == '__main__':
    test_write_csv()
    print('Module func passed all tests.')