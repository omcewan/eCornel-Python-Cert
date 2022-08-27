#!/usr/bin/env python
"""
Assess the third free-response question.

This file is insecurely available to students, but if they find it and modify it, they
really did not need this course.

Author: Walker M. White
Date:   July 1, 2019
"""
import os, requests, sys
import subprocess

answer  = os.environ['CODIO_FREE_TEXT_ANSWER']
#answer = sys.argv[1] if len(sys.argv) > 1 else ''

answer = answer.strip().split('\n')
answer = list(filter(lambda x : len(x) > 0, answer))
for pos in range(len(answer)):
    answer[pos] = answer[pos].rstrip()

while len(answer) > 0 and answer[0] == '':
    del answer[0]
while len(answer) > 0 and answer[-1] == '':
    del answer[-1]


result  = True
if len(answer) == 0:
    print('The answer should not be empty.')
    result = False
elif len(answer) == 6:
    print('Make sure you commented out the assignment to x.')
    result = False
elif len(answer) != 8:
    print('The answer should take up eight lines.')
    result = False
elif answer[0] != 'Traceback (most recent call last):':
    print("The output should start with 'Traceback'.")
    result = False
elif not 'File "funcs.py", line 71, in' in answer[1]:
    print("Make sure the assignment to variable y is still at line 71.")
    result = False
elif not 'File "funcs.py", line 64, in' in answer[3]:
    print("Make sure the call to 'numerator' is still at line 64.")
    result = False
elif not 'File "funcs.py", line 30, in' in answer[5]:
    print("Make sure the return statement for 'numerator' is still at line 30.")
    result = False
elif not 'ValueError: invalid literal for int()' in answer[-1]:
    print('The output should end with the error type.')
    result = False


if result:
    print('Correct')
else:
    sys.exit(1)