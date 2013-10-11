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
This trial module watches /home recursively, for sake of simplicity, 
say we watch for modifying infinitely and executes a callback whenever 
a modifying event occurs.
"""
import os
import sys
import pyinotify

def watch_folder(folder, on_changed, args=None):
    """
    This method watches the folder, @folder, for changes
    and calls the method, @on_changed, if there is any change
    (file/folder create/remove, modify file etc.) in the folder.
    
    @folder: to be watched
    @on_changed : the function to call if there is a change
    @args       : extra arguments to pass @on_changed
    """
    handler = EventHandler(on_changed, args)
    start_loop(folder, handler, True)


class EventHandler(pyinotify.ProcessEvent):
    
    def __init__(self, on_changed=None ,args=None):
        self.on_changed = on_changed
        self.args = args
    
    def __process_CHANGE(self, event, event_type):
        if self.on_changed:
            # if available call the registered callback (self.on_changed)
            self.on_changed(event.pathname, self.args, event_type)
        else:
            # inform the user by printing the change
            print '%s: %s' % (event.pathname, event_type)
    
    
    def process_IN_MODIFY(self, event):
        """
        This method prints an informative message if any file 
        is modified, then executes a callback responsible for rsyncing.
        """
        self.__process_CHANGE(event, 'modify')
    
    def process_IN_CREATE(self, event):
        """
        This method prints an informative message if any file 
        is created, then executes a callback responsible for rsyncing.
        """
        self.__process_CHANGE(event, 'create')
    
    def process_IN_DELETE(self, event):
        """
        This method prints an informative message if any file 
        is deleted, then executes a callback responsible for rsyncing.
        """
        self.__process_CHANGE(event, 'delete')

    def process_IN_MOVED_FROM(self, event):
        """
        This method prints an informative message if any file 
        is moved from somewhere, then executes a callback responsible for rsyncing.
        """
        self.__process_CHANGE(event, 'moved_from')

    def process_IN_MOVED_TO(self, event):
        """
        This method prints an informative message if any file 
        is moved to somewhere, then executes a callback responsible for rsyncing.
        """
        self.__process_CHANGE(event, 'moved_to')

    def process_default(self, event):
        """
        This method prints and informative message for any other
        file/folder change event other than the ones listed above. 
        """
        self.__process_CHANGE(event, 'unknown')


def start_loop(folder, handler, recursive):
    wm = pyinotify.WatchManager()
    notifier = pyinotify.Notifier(wm, handler)
    mask = pyinotify.IN_CREATE | pyinotify.IN_DELETE | pyinotify.IN_MODIFY \
            | pyinotify.IN_MOVED_FROM | pyinotify.IN_MOVED_TO
    wdd = wm.add_watch(folder, mask, rec=recursive)
    notifier.loop() 


def usage(args):
    print 'usage: %s [folder] [-r] [-h]' % args[0]
    print '       %s /home -r' % args[0]

def test(args):
    if '-h' in args:
        usage(args)
        return
    folder = '/home'
    recursive = '-r' in args
    if len(args) > 1 and os.path.exists(args[1]):
        folder = args[1]
    start_loop(folder, EventHandler(), recursive)

if __name__ == '__main__':
    test(sys.argv)
