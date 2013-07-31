"""
This module synchronizes files in one folder to another one. 
"""
import subprocess

def sync_folder(source, target, excluded):
    """
    This method synchronize @source folder to @target folder
    using "rsync". 
    """
    # TODO: exclude calismiyor sanirim (bakabilir misin?)
    rsync_cmd = 'rsync -rtvu --delete --exclude "%s" %s/ %s/' % (excluded, source, target)
    print rsync_cmd
    p = subprocess.Popen(rsync_cmd, stdout=subprocess.PIPE, shell=True)
    status = p.wait()
    output = p.stdout.read()
    #status = os.system(rsync_cmd)
    return status == 0 # success

