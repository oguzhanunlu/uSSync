"""
This module watches a folder for changes and executes a callback
whenever a change occurs.
"""
import os
import sys
import time

def watch_folder(folder, on_changed, args=None):
    """
    This method watches the folder, @folder, for changes
    and calls the method, @on_changed, if there is any change
    (file/folder create/remove, modify file etc.) in the folder.
    
    @folder: to be watched
    @on_changed : the function to call if there is a change
    @args       : extra arguments to pass @on_changed
    """
    while True:
        # check if there is any change in @folder
        #changed = bool(random.randint(0, 1))
        #if changed:
        if args:
            on_changed(folder, args)
        else:
            on_changed(folder)
        time.sleep(2) # check every one second

