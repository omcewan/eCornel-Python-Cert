"""  
A completed test script for the time functions.

Notice how complicated testing is now.  To test that the return value of a function is
correct, we need to test (1) its type and (2) each attribute separately.  Because 
functions can now modify the arguments, we also need to verify that arguments are not
modified unless the specification specifically says they are.

Author: Walker M. White
Date: August 9, 2019
"""
import funcs
import introcs
import os.path

# The proper contents for file1.json
FILE1 = {
    "2018-01-01T00:00:00-05:00": {
        "visibility": {
            "prevailing": 1.75,
            "units": "SM"
        },
        "wind": {
            "speed": 13.0,
            "crosswind": 5.0,
            "units": "KT"
        },
        "temperature": {
            "value": -15.0,
            "units": "C"
        },
        "sky": [
            {
                "cover": "clouds",
                "type": "broken",
                "height": 1200.0,
                "units": "FT"
            },
            {
                "type": "overcast",
                "height": 1800.0,
                "units": "FT"
            }
        ],
        "weather": [
            "light snow",
            "mist"
        ],
        "code": "201801010456Z"
    },
    "2017-12-31T23:00:00-05:00": {
        "visibility": {
            "prevailing": 1.75,
            "units": "SM"
        },
        "wind": {
            "speed": 13.0,
            "crosswind": 5.0,
            "units": "KT"
        },
        "temperature": {
            "value": -15.0,
            "units": "C"
        },
        "sky": [
            {
                "cover": "clouds",
                "type": "broken",
                "height": 1300.0,
                "units": "FT"
            },
            {
                "type": "overcast",
                "height": 2200.0,
                "units": "FT"
            }
        ],
        "weather": [
            "light snow",
            "mist"
        ],
        "code": "201801010356Z"
    },
    "2017-12-31T22:00:00-05:00": {
        "visibility": {
            "prevailing": 3.0,
            "units": "SM"
        },
        "wind": {
            "speed": 11.0,
            "crosswind": 7.0,
            "units": "KT"
        },
        "temperature": {
            "value": -15.0,
            "units": "C"
        },
        "sky": [
            {
                "type": "overcast",
                "height": 1300.0,
                "units": "FT"
            }
        ],
        "weather": [
            "light snow",
            "mist"
        ],
        "code": "201801010317Z"
    },
    "2017-12-31T21:00:00-05:00": {
        "visibility": {
            "prevailing": 10.0,
            "units": "SM"
        },
        "wind": {
            "speed": 10.0,
            "crosswind": 7.0,
            "units": "KT"
        },
        "temperature": {
            "value": -16.1,
            "units": "C"
        },
        "sky": [
            {
                "type": "overcast",
                "height": 1700.0,
                "units": "FT"
            }
        ],
        "code": "201801010156Z"
    }
}


# The proper contents for file2.json
FILE2 = [
    {
        "cover": "clouds",
        "type": "broken",
        "height": 1200.0,
        "units": "FT"
    },
    {
        "type": "overcast",
        "height": 1800.0,
        "units": "FT"
    }
]


def unindent_json(text):
    """
    Returns an unindented version of a JSON string.
    
    This function is used for comparisons.  It allows us to check if the only
    thing wrong was indentation.
    """
    import json
    return json.dumps(json.loads(text))


def test_read_json():
    """
    Test procedure for the function read_json()
    """
    print('Testing read_json()')
    
    # Access the file relative to this one, not the user's terminal
    parent = os.path.split(__file__)[0]
    
    # First test
    fpath = os.path.join(parent,'files','readjson1.json')
    data  = funcs.read_json(fpath)
    
    introcs.assert_equals(dict, type(data))
    introcs.assert_equals(FILE1, data)
    
    # Second test
    fpath  = os.path.join(parent,'files','readjson2.json')
    data  = funcs.read_json(fpath)
    
    introcs.assert_equals(list, type(data))
    introcs.assert_equals(FILE2, data)


def test_write_json():
    """
    Test procedure for the function write_json()
    """
    print('Testing write_json()')
    
    # Access the file relative to this one, not the user's terminal
    parent = os.path.split(__file__)[0]
    
    # First test (erase any existing file)
    fpath  = os.path.join(parent,'files','temp1.json')
    open(fpath,'w').close()
    funcs.write_json(FILE1,fpath)
    
    # Check file was created
    introcs.assert_true(os.path.exists(fpath))
    
    file = open(fpath)
    actual  =  file.read()
    file.close()
    
    file = open(os.path.join(parent,'files','readjson1.json'))
    correct = file.read()
    file.close()
    
    # Check to see if they are the same WITHOUT indentation
    introcs.assert_equals(unindent_json(correct),unindent_json(actual))
    # Check to see if they are the same WITH indentation
    introcs.assert_equals(correct,actual)
    
    # Second test (erase any existing file)
    fpath  = os.path.join(parent,'files','temp2.json')
    open(fpath,'w').close()
    funcs.write_json(FILE2,fpath)
    
    # Check file was created
    introcs.assert_true(os.path.exists(fpath))
    
    file = open(fpath)
    actual  =  file.read()
    file.close()
    
    file = open(os.path.join(parent,'files','readjson2.json'))
    correct = file.read()
    file.close()
    
    # Check to see if they are the same WITHOUT indentation
    introcs.assert_equals(unindent_json(correct),unindent_json(actual))
    # Check to see if they are the same WITH indentation
    introcs.assert_equals(correct,actual)


if __name__ == '__main__':
    test_read_json()
    test_write_json()
    print('Module funcs passed all tests.')