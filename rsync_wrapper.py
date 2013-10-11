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
import shlex
import subprocess

class Status(object):
    def __init__(self, values):
        self.transfered = values[0]
        self.percentage = values[1]
        self.speed = values[2]
        self.remaining = values[3]
    
    def __str__(self):
        return '%s %s%% %s %s' % \
            (self.transfered, self.percentage, self.speed, self.remaining)

class Rsync(object):
    CMD = 'rsync -rtvuh --progress --delete --exclude "%s" %s/ %s/ | unbuffer -p cat'
    
    def __init__(self, source, target, excluded='', on_progress=None):
        self.source = source
        self.target = target
        self.on_progress = on_progress
        self.excluded = excluded
        self.cmd = Rsync.CMD % (excluded, source, target)
        self.current_status = Status(['0', '0', '0.00kB/s', 'N/A'])
        self.current_file = None
        self.finished = False
        self.transfered_files = []
    
    def run(self):
        self.finished = False
        self.transfered_files = []
        p = subprocess.Popen(self.cmd, stdout=subprocess.PIPE, shell=True)
        while True:
            line = p.stdout.readline()
            if not line:
                break
            status = self.parse_line(line)
            if status:
                self.current_status = status
                if self.on_progress:
                    self.on_progress(self.get_progress())
        status = p.wait()
        self.finished = True
        return status
    
    def parse_line(self, line):
        if '%' in line:
            fields = shlex.split(line)
            if len(fields) < 4:
                return None
            fields[1] = fields[1].replace('%', '')
            status = Status(fields)
            return status
        if line[0].isalnum() and len(line.split()) == 1:
            if self.current_file is not None:
                self.status = Status(['', '100', '0.00kB/s', '0:00:00'])
            self.current_file = line.strip()
            self.transfered_files.append(self.current_file)
        return None

    def get_progress(self):
        if self.current_file is None:
            return None
        return (self.current_file, self.current_status)



def check_progress(rsync):
    import time
    while not rsync.finished:
        progress = rsync.get_progress()
        if progress:
            current_file = progress[0]
            current_status = progress[1]
            print '%s %s' % (current_file, current_status)
        time.sleep(0.2)

def on_progress(progress):
    current_file = progress[0]
    current_status = progress[1]
    print '%s %s' % (current_file, current_status)

def test(source_folder, target_folder):
    import thread
    #rsync = Rsync(source_folder, target_folder)
    #thread.start_new_thread(check_progress, (rsync,))
    rsync = Rsync(source_folder, target_folder, '', on_progress)
    rsync.run()
    print 'transfered:', ' '.join(rsync.transfered_files)

def test_main(args):
    source_folder = '~/Desktop/source'
    target_folder = '~/Desktop/target'
    if len(args) >= 2:
        source_folder = args[0]
        target_folder = args[1]
    test(source_folder, target_folder)

if __name__ == '__main__':
    import sys
    test_main(sys.argv[1:])
