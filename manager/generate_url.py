#! /usr/bin/env python

import os
import sys
import yaml
import sqlite3
import random

with open(u'%s/manager_conf.yaml' % os.path.split(os.path.realpath(__file__))[0], u'r') as f:
    conf = yaml.safe_load(f)

batch_count = 50
name_db = conf[u'name_db']
url_number = conf[u'url_number']

server_list = []
with open(u'/tmp/server_ip', u'r') as f:
    for eachline in f:
        ip = eachline.strip()
        if ip:
            server_list.append(ip)

cx = sqlite3.connect(name_db)
cu = cx.cursor()

cu.execute(u'select * from name')
i = 0
server_number = len(server_list)

while True:
    rets = cu.fetchmany(url_number)
    if len(rets) < url_number:
        break
    f_download = open(u'/srv/salt/url/download_url_%d.txt' % i, u'w')
    f_upload = open(u'/srv/salt/url//upload_url_%d.txt' % i, u'w')
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
        
