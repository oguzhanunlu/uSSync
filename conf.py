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
import sys

def parse_conf(lines):
    conf = {}
    for line in lines:
        line = line.strip()
        index = line.find('#')
        if index != -1:
            line = line[:index]
        if not line:
            continue
        fields = line.split()
        if len(fields) != 2:
            continue
        key = fields[0].strip()
        val = fields[1].strip()
        conf[key] = val
    return conf

def read_conf(filename):
    with open(filename) as f:
        lines = f.readlines()
        conf = parse_conf(lines)
        return conf

def write_conf(conf, stream=sys.stdout):
    for key in sorted(conf):
        print >> stream, key, conf[key]

def get_sync_module(conf):
    module = conf['sync']
    return __import__('sync.' + module, fromlist=[module])

def get_watch_module(conf):
    module = conf['watch']
    return __import__('watch.' + module, fromlist=[module])
