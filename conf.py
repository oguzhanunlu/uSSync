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

