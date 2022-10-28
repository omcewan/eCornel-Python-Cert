"""
Partially completed test script for keyword expansion

Author: Orlando McEwan
Date: 10/27/2022
"""
import introcs
import func


def test_circ_area():
    """
    Test procedure for function circ_area().
    """
    print('Testing circ_area()')

    result = func.circ_area(radius=3)
    introcs.assert_floats_equal(28.27433, result)

    result = func.circ_area(radius=2)
    introcs.assert_floats_equal(12.56637, result)

    result = func.circ_area(diameter=4)
    introcs.assert_floats_equal(12.56637, result)

    # Test for crashes
    try:
        func.circ_area()
        introcs.assert_true(False)  # We should never reach this line!
    except:
        pass

    try:
        func.circ_area(radius=3, diameter=6)
        introcs.assert_true(False)  # We should never reach this line!
    except:
        pass

    # Add a test with additional arguments
    result = func.circ_area(**{"radius": 3, "foo": 20, "bar": 10})


if __name__ == '__main__':
    test_circ_area()
    print('Module func passed all tests.')
