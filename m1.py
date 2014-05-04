#! /usr/bin/env python

import os
import json
import yaml
import signal
import logging
import sqlite3
from flask import Flask, request, redirect, url_for, render_template, abort, Response

with open(u'manager_conf.yaml') as f:
    conf = yaml.safe_load(f)

pid_file = conf[u'pid_file']
instance_db = conf[u'instance_db']
server_number = conf[u'server_number']
client_number = conf[u'client_number']
server_list = conf[u'server_list']
client_list = conf[u'client_list']

logging.basicConfig(filename = u'/tmp/manager_log.txt', level = logging.INFO)

cx = sqlite3.connect(instance_db)
cu = cx.cursor()
cu.execute(u'creat table instance(ip_addr vchar(20) primary key, role vchar(10))')
cx.commit()
cu.close()


app = Flask(__name__)

def make_resp(data, status):
    js = json.dumps(data)
    resp = Response(js, status=status, mimetype='application/json')
    return resp

@app.route(u'/', methods=[u'GET', u'POST'])
def index():
    return u'un-init'

@app.route(u'/notice', methods=[u'GET', u'POST'])
def notice():
    if request.method == u'POST':
        try:
            data = request.json
        except Exception, e:
            ret_data = {u'reason': u'not json format'}
            return make_resp(ret_data, 400)
        logging.info(u'data: %s' % data)
        if u'ip_addr' not in data:
            ret_data = {u'reason': u'no ip_addr'}
            return make_resp(ret_data, 400)
        ip_addr = data[u'ip_addr']
        if u'role' not in data:
            ret_data = {u'reason': u'no role'}
            return make_resp(ret_data, 400)
        role = data[u'role']
        cu = cx.cursor()
        cu.execute(u'insert into instance values("%s", "%s")' % (ip_addr, role))
        cx.commit()
        cu.close()

        cu = cx.curose()
        cu.execute(u'select count(*) from instance')
        number = cu.fetchall()[0][0]
        cu.close()
        if number == (server_number + client_number):
            try:
                with open(pid_file, u'r') as f:
                    task_pid = int(f.read().strip())
            except Exception, e:
                ret_data = {u'reason': u'pid_file %s' % e}
                return make_resp(ret_data, 500)
            os.kill(task_pid, signal.SIGUSR1)
        ret_data = {u'reason': u'success'}
        return make_resp(ret_data, 200)
    cu = cx.cursor()
    cu.execute(u'select * from instance')
    ret = cu.fetchall()
    cu.close()
    return u'%s' % ret
