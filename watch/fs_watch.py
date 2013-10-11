# This file is part of uSSync. 
# 
# This program is free software: you can redistribute it and/or modify 
# it under the terms of the GNU General Public License as published by 
# the Free Software Foundation, either version 3 of the License, or 
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful, 
# but WITHOUT ANY WARRANTY; without even the implied warranty of 
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the 
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License 
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
# 
# Copyright 2013 Erdal Sivri, Oguzhan Unlu
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

