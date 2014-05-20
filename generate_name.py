#! /usr/bin/env python

import sys
import signal
import names
import sqlite3

name_count = int(sys.argv[1])
name_db = sys.argv[2]

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

print(u'try: %d valid: %d' % (try_count, i))
cx.commit()
cu.close()
cx.close()
