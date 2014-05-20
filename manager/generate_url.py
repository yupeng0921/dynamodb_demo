#! /usr/bin/env python

import sys
import yaml
import sqlite3
import random

with open(u'manager_conf.yaml') as f:
    conf = yaml.safe_load(f)

batch_count = 50
url_dir = u'url'
name_db = conf[u'name_db']
url_number = conf[u'url_number']
# server_list = conf[u'server_list']

server_list = []
server_list_file = sys.argv[1]
# change "ip-172-31-5-122.ap-northeast-1.compute.internal:"
# to 172.31.5.122
with open(server_list_file) as f:
    for eachline in f:
        ip = eachline[3:].split(u'.')[0].replace(u'-',u'.')
        server_list.add(ip)

cx = sqlite3.connect(name_db)
cu = cx.cursor()

cu.execute(u'select * from name')
i = 0
server_number = len(server_list)

while True:
    rets = cu.fetchmany(url_number)
    if len(rets) < url_number:
        break
    f_download = open(u'%s/download_url_%d.txt' % (url_dir, i), u'w')
    f_upload = open(u'%s/upload_url_%d.txt' % (url_dir, i), u'w')
    i += 1
    j = 0
    for ret in rets:
        name = ret[0]
        server = server_list[j]
        j += 1
        j %= server_number
        score = random.randint(100, 1000)
        url = u'http://%s/download/%s\n' % (server, name)
        f_download.write(url)
        url = u'http://%s/upload/%s?score=%d\n' % (server, name, score)
        f_upload.write(url)
    f_download.close()
    f_upload.close()
        
