#!/usr/local/bin/python3
"""
The grading function the module

This file is to be stored in a secure location.

Author: Walker M. White
Date:   July 31, 2018
"""
import os.path, sys
import verifier

sys.path.append('/home/codio/workspace')
sys.path.append('/usr/share/codio/assessments')
from lib.grade import send_grade


WORKSPACE = [os.path.expanduser('~'),'workspace']
#WORKSPACE = []


def grade():
    """
    Processes the student submission
    
    Parameter name: The file name
    Precondition: name is a string
    """
    try:
        path = os.path.join(*WORKSPACE,'feedback.txt')
        feedback = open(path,'w')
    except:
        print('Failed to open feedback file')
        return
    
    total = 0
    feedback.write('Feedback\n========\n')
    total += verifier.grade(feedback)*100
    feedback.close()
    send_grade(total)
    print('Autograder completed successfully')


if __name__ == '__main__':
    grade()
