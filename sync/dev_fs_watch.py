"""
This trial module watches /home recursively, for sake of simplicity, say we watch for modifying infinitely and executes a callback whenever a modifying event occurs.
"""
import pyinotify
import subprocess
import fs_sync

wm = pyinotify.WatchManager()

mask = pyinotify.IN_CREATE | pyinotify.IN_DELETE | IN_MODIFY 

class EventHandler(pyinotify.ProcessEvent):

    def process_IN_MODIFY(self, event):
    """
    This method prints an informative message if any file is modified, then executes a callback responsible for rsyncing.
    """
        print "Modifying:", event.pathname
		sync_folder(source,target) 
    
    def process_IN_CREATE(self, event):
    """
    This method prints an informative message if any file is created, then executes a callback responsible for rsyncing.
    """
        print "Creating:", event.pathname
        sync_folder(source,target)

    def process_IN_DELETE(self, event):
    """
    This method prints an informative message if any file is deleted, then executes a callback responsible for rsyncing.
    """
        print "Removing:", event.pathname
        sync_folder(source,target)
        

handler = EventHandler()
notifier = pyinotify.Notifier(wm, handler)
wdd = wm.add_watch('/home', mask, rec=True)

notifier.loop() 
