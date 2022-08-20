#!/usr/bin/env python
"""
Assess the first free-response question.

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
elif len(answer) < 9:
    print('The answer should take up at least nine lines.')
    result = False
elif answer[0] != 'Testing second_in_list':
    print("The output is missing 'Testing second_in_list'.")
    result = False
elif not 'NameError: name' in answer[-1]:
    print('The output is not correct (the last line should be the error type).')
    result = False
elif not 'Traceback (most recent call last):' in answer:
    print('The output is missing the error report.')
    result = False


if result:
    print('Correct')
else:
    sys.exit(1)