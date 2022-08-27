#!/usr/bin/env python
"""
Assess the fourth free-response question.

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
elif len(answer) != 1:
    print('The answer should only be a single line.')
    result = False
elif 'File "funcs.py", line 64, in' in answer[0]:
    print("Go back and read the preconditions.")
    result = False
elif 'File "funcs.py", line 71, in' in answer[0]:
    print("Go back and read the preconditions.")
    result = False
elif not 'File "funcs.py", line 30, in numerator' in answer[0]:
    if '30' in answer[0]:
        print("Give the entire line of the error message, not just the line number.")
    elif not 'line' in answer[0]:
        print("That is not a line mumber.")
    else:
        print("That is not the line with the error.")
    result = False


if result:
    print('Correct')
else:
    sys.exit(1)