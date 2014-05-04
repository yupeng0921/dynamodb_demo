#! /usr/bin/env python

import sys
import yaml
import signal
import names
import sqlite3

with open(u'name_conf.yaml') as f:
    conf = yaml.safe_load(f)

name_count = conf[u'name_count']
name_db = conf[u'name_db']

cx = sqlite3.connect(name_db)
cu = cx.cursor()
cu.execute(u'create table name(name vchar(100) primary key)')

def close_and_exit(a,b):
    cx.commit()
    cu.close()
    cx.close()
    sys.exit(0)
signal.signal(signal.SIGINT, close_and_exit)

i = 0
try_count = 0
while i < name_count:
    name = names.get_full_name().replace(u' ', u'_')
    try_count += 1
    try:
        cu.execute(u'insert into name values("%s")' % name)
    except Exception, e:
        pass
    else:
        i += 1
    if (try_count % 100) == 0:
        print(u'try: %d valid: %d' % (try_count, i))
        cx.commit()

cx.commit()
cu.close()
cx.close()
