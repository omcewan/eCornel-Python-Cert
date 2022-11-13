"""
Refresh key student-accessible data files by copying from the .guides folder tree.
Called from a button on step 2.

Author: Seth Taylor
Date: 2/5/2022
"""
 
import os
import shutil

source_dir = [".guides", "tests", "testfiles"]
dest_dirs = [
    ["auditor", "tests"],
    ["KITH-2017"]
    ]

files = [
    'daycycle.json', 'fleet.csv', 'instructors.csv', 'lessons.csv',
    'minimums.csv', 'repairs.csv', 'students.csv', 'weather.json'
    ]

for dest_dir in dest_dirs:
    print("Starting to reset data files in %s." % os.path.join(*dest_dir))
    for file in files:
        full_source = os.path.join(*source_dir, file)
        full_dest = os.path.join(*dest_dir, file)
        shutil.copy(full_source, full_dest)
        print("  Reset", full_dest)
    print("Finished resetting data files in %s." % os.path.join(*dest_dir))
