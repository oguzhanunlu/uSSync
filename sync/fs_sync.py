"""
This module synchronizes files in one folder to another one. 
"""
import subprocess
from rsync_wrapper import Rsync

def sync_folder(source, target, excluded, on_progress=None):
    """
    This method synchronize @source folder to @target folder
    using "rsync". 
    """
    rsync = Rsync(source, target, excluded, on_progress)
    status = rsync.run()
    return status == 0 # success

