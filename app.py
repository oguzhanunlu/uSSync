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
#! /usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys

import conf
import sync
import watch
from exclude import Exclude


class USSyncApp(object):
    def __init__(self):
        self.sync_module = None
        self.exclude = None
    
    def print_info(self, message, stream=sys.stdout):
        print >> stream, '[info]: %s' % message
   
    def print_error(self, message, stream=sys.stderr):
        print >> stream, '[error]: %s' % message

    def on_changed(self, file_or_folder, args, change_type):
        """
        callback executed if there is any change in @folder_name
        """
        #self = args[0]
        if self.exclude and self.exclude.is_excluded(file_or_folder):
            self.print_info('%s in ignore/exclude list' % file_or_folder)
            return
        self.sync()
    
    def sync(self):
        source_folder = self.source_folder
        target_folder = self.target_folder
        on_progress = self.on_progress
        if self.sync_module:
            excluded = self.exclude.get_excluded() if self.exclude is not None else ''
            success = self.sync_module.sync_folder(source_folder, target_folder, excluded, on_progress)
            if success:
                self.print_info('sync ok :)')
            else:
                self.print_error('error in sync :(')
            self.success = success
        else:
            raise Exception('sync_module not loaded')
    
    def create_default_conf(self, conf_file):
        confs = {
            'watch': 'dev_fs_watch',
            'sync': 'fs_sync',
            'source_folder': '~/source',
            'target_folder': '~/target',
            'verbose': 'True',
            'checksum': 'False',
            'preserve_permissions': 'True',
            'preserve_time': 'True',
            'disable_recursion': 'False',
        }
        with open(conf_file, 'w+') as f:
            conf.write_conf(confs, f)
    
    def run(self, conf_file, on_progress):
        if not os.path.exists(conf_file):
            self.create_default_conf(conf_file)
        self.on_progress = on_progress
        # read configuration file
        self.configuration = conf.read_conf(conf_file)
        self.source_folder = os.path.expanduser(self.configuration['source_folder'])
        self.target_folder = os.path.expanduser(self.configuration['target_folder'])
        exclude_file = os.path.expanduser(self.configuration.get('ignore_file') or '.uSSyncignore')
        self.exclude = Exclude(exclude_file)
        self.sync_module = conf.get_sync_module(self.configuration)
        watch_module = conf.get_watch_module(self.configuration)
        # start the main loop
        watch_module.watch_folder(self.source_folder, self.on_changed, [self])
    
    def run_async(self, conf_file, on_progress):
        import thread
        self.on_progress = on_progress
        self.background_thread = thread.start_new_thread(self.run, (conf_file, on_progress))
    

def on_progress(progress):
    current_file = progress[0]
    current_status = progress[1]
    print '%s %s' % (current_file, current_status)


def usage(args):
    print 'usage: %s [<config-file>]' % args[0]

def main(args):
    if '-h' in args:
        usage(args)
        return
    conf_file = os.path.expanduser('~/app.conf')
    if len(args) >= 2:
        conf_file = args[1]
    app = USSyncApp()
    app.run(conf_file, on_progress)

if __name__ == '__main__':
    main(sys.argv)
