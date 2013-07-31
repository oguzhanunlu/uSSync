#! /usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys

import conf
import sync
import watch
from exclude import Exclude

sync_module = None
exclude = None

def print_info(message, stream=sys.stdout):
    print >> stream, '[info]: %s' % message

def print_error(message, stream=sys.stderr):
    print >> stream, '[error]: %s' % message

def on_changed(file_or_folder, args, change_type):
    """
    callback executed if there is any change in @folder_name
    """
    print '%s: %s' % (file_or_folder, change_type)
    if sync_module:
        if exclude and exclude.is_excluded(file_or_folder):
            print_info('%s in ignore/exclude list' % file_or_folder)
        else:
            excluded = exclude.get_excluded() if exclude is not None else ''
            success = sync_module.sync_folder(args[0], args[1], excluded)
            if success:
                print_info('sync ok :)')
            else:
                print_error('error in sync :(')
    else:
        print_error('sync_module not loaded')
        sys.exit(1)


def usage(args):
    print 'usage: %s [<config-file>]' % args[0]

def main(args):
    if '-h' in args:
        usage(args)
        return
    conf_file = 'app.conf'
    if len(args) == 2:
        conf_file = args[1]
    # read configuration file
    configuration = conf.read_conf(conf_file)
    source_folder = os.path.expanduser(configuration['source_folder'])
    target_folder = os.path.expanduser(configuration['target_folder'])
    exclude_file = os.path.expanduser(configuration.get('ignore_file') or '.uSSyncignore')
    global exclude
    exclude = Exclude(exclude_file)
    global sync_module
    sync_module = conf.get_sync_module(configuration)
    watch_module = conf.get_watch_module(configuration)
    # start the main loop
    watch_module.watch_folder(source_folder, on_changed, [source_folder, target_folder])

if __name__ == '__main__':
    main(sys.argv)

