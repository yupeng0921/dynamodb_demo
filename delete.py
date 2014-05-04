#! /usr/bin/env python

import sys
import yaml
import boto
import boto.dynamodb2
from boto.dynamodb2.table import Table

with open(u'manager_conf.yaml') as f:
    conf = yaml.safe_load(f)

table_name = conf[u'table_name']
region = conf[u'region']

conn = boto.dynamodb2.connect_to_region(region)
table = Table(table_name, connection=conn)

items = table.scan()

count = 0
for item in items:
    item.delete()
    count += 1
    if ((count % 100) == 0):
        print(u'delete count: %d' % count)

print(u'total delete count: %d' % count)
                            
