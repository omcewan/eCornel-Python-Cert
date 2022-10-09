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

correct = """
Start first
Start first try
Start second
Start second try
End second try
Done second
End first try
Done first
0
"""
correct = correct.strip().split('\n')
for pos in range(len(correct)):
    correct[pos] = correct[pos].rstrip()


result  = True
if len(answer) == 0:
    print('The answer should not be empty.')
    result = False
elif len(answer) != len(correct):
    print('The answer should take up %d lines.' % len(correct))
    if correct[-1] not in answer:
        print("The output is missing the last line with the return value.")
    result = False
else:
    pos = 0
    while pos < len(correct) and result:
        if correct[pos] not in answer:
            print("The output is missing %s." % correct[pos])
            result = False
        pos += 1


if result:
    print('Correct')
else:
    sys.exit(1)