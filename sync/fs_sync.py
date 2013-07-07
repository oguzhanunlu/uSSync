"""
This module synchronizes files in one folder to another one. 
"""
import subprocess

def sync_folder(source, target):
    """
    This method synchronize @source folder to @target folder
    using "rsync". 
    """
    rsync_cmd = 'rsync -avz %s/* %s' % (source, target)
    p = subprocess.Popen(rsync_cmd, stdout=subprocess.PIPE, shell=True)
    status = p.wait()
    output = p.stdout.read()
    #status = os.system(rsync_cmd)
    return status == 0 # success

