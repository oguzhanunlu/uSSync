#! /usr/bin/python
# -*- coding: utf-8 -*-

import sys

import conf
import sync
import watch

sync_module = None

def on_changed(folder_name, args):
    """
    callback executed if there is any change in @folder_name
    """
    success = sync_module.sync_folder(folder_name, args[0])
    if success:
        print 'sync ok :)'
    else:
        print 'error in sync :('


def usage(args):
    print 'usage: %s [<config-file>]' % args[0]
    sys.exit(1)

def main(args):
    if '-h' in args:
        usage(args)
    conf_file = 'app.conf'
    if len(args) == 2:
        conf_file = args[1]
    # read configuration file
    configuration = conf.read_conf(conf_file)
    source_folder = configuration['source_folder']
    target_folder = configuration['target_folder']
    global sync_module
    sync_module = conf.get_sync_module(configuration)
    watch_module = conf.get_watch_module(configuration)
    # start the main loop
    watch_module.watch_folder(source_folder, on_changed, [target_folder])

if __name__ == '__main__':
    main(sys.argv)

