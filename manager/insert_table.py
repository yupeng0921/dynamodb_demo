#! /usr/bin/env python

import sys
import time
import yaml
import sqlite3
import random
import boto
import boto.dynamodb2
from boto.dynamodb2.table import Table

with open(u'manager_conf.yaml') as f:
    conf = yaml.safe_load(f)

table_name = conf[u'table_name']
region = conf[u'region']
name_db = conf[u'name_db']
count_per_user = conf[u'count_per_user']
batch_count = conf[u'batch_count']

year = 2014
last_month = 4
init_date = 0
def generate_date():
    month = random.randint(1,last_month)
    day = random.randint(1,28)
    hour = random.randint(0,23)
    minute = random.randint(0,59)
    second = random.randint(0,59)
    date = u'%04d%02d%02d%02d%02d%02d' % (year, month, day, hour, minute, second)
    return date

def generate_score():
    score = random.randint(100,1000)
    return score

def do_insert():
    conn = boto.dynamodb2.connect_to_region(region)
    table = Table(table_name, connection=conn)
    cx = sqlite3.connect(name_db)
    cu = cx.cursor()
    count = 0
    cu.execute("select * from name")
    test_count=1000
    while True:
        rets = cu.fetchmany(batch_count)
        if len(rets) <= 0:
            break
        with table.batch_write() as batch:
            for ret in rets:
                name = ret[0]
                dates = []
                while len(dates) < count_per_user:
                    date = generate_date()
                    if date in dates:
                        continue
                    dates.append(date)
                for date in dates:
                    score = generate_score()
                    batch.put_item(data={u'name':name, u'date':date, u'score':score})
                    count += 1
        print(count)
    
if __name__ == u'__main__':
    do_insert()
