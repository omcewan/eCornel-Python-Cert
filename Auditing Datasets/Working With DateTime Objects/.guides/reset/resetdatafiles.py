"""
Refresh the daycycle.json files  copying from the .guides folder tree.
Called from buttons in the guide.

Author: Seth Taylor
Date: 2/5/2022
"""
 
import os
import shutil

source_dir = [".guides", "reset"]
dest_dirs = [
    ["exercise4"],
    ["exercise5"]
    ]

files = [ 'daycycle.json' ]

for dest_dir in dest_dirs:
    print("Starting to reset data files in %s." % os.path.join(*dest_dir))
    for file in files:
        full_source = os.path.join(*source_dir, file)
        full_dest = os.path.join(*dest_dir, file)
        shutil.copy(full_source, full_dest)
        print("  Reset", full_dest)
    print("Finished resetting data files in %s." % os.path.join(*dest_dir))
