"""
Trace statements illustrating control statement flow

Trace statements are just print statements that tell us
where we are in the code.  They are distinct from a
watch, which tells us the current contents of a variable.

Author: Walker M. White
Date:   March 30, 2019
"""


def max2(x,y):
    """
    Returns: max of x, y

    This function shows the flow of if-else.

    Parameter x: first value
    Precondition: x is a number

    Parameter y: second value
    Precondition: y is a number
    """
    # Put max of x, y in z
    print('before if')          # trace
    if x > y:
        print('if x>y')         # trace
        z  = x
        print('z is '+str(z))   # watch
    else:
        print('else x<=y')      # trace
        z  = y
        print('z is '+str(z))   # watch
    print('after if')           # trace
    return z


def max3(x,y,z):
    """
    Returns: max of x, y, z

    This function shows the flow of if-elif-else.

    Parameter x: first value
    Precondition: x is a number

    Parameter y: second value
    Precondition: y is a number

    Parameter z: third value
    Precondition: z is a number
    """

    # Put max of x, y, z in w
    print('before if')              # trace
    if x > y and x > z:
        print('if x>y and x>z')     # trace
        w  = x
        print('w is '+str(w))       # watch
    elif y > z:
        print('elif y>z and y>=x')  # trace
        w  = y
        print('w is '+str(w))       # watch
    else:
        print('else z>=x and z>=y') # trace
        w  = z
        print('w is '+str(w))       # watch
    print('after if')               # trace
    return w
