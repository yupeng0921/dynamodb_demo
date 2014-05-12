#! /usr/bin/env python

import time
import yaml
import json
import copy
import random
import requests
from flask import Flask, request, redirect, url_for, render_template, abort, Response

with open(u'manager_conf.yaml') as f:
    conf = yaml.safe_load(f)

pid_file = conf[u'pid_file']
server_list = conf[u'server_list']
client_list = conf[u'client_list']
concurrent_number = int(conf[u'concurrent_number'])

app = Flask(__name__)

idle_list = []
reader_list = []
writer_list = []

def stop_all():
    headers = {'content-type': 'application/json'}
    tmp_list = []
    for ip in client_list:
        url = u'http://%s' % ip
        data = {u'action': u'stop'}
        data = json.dumps(data)
        ret = requests.post(url, data=data, headers=headers)
        print(ret)
        idle_list.append(ip)

stop_all()


task_index = random.randint(0,500)
def get_task_index():
    global task_index
    task_index += 1
    task_index %= 500
    return task_index

def increase_reader(num):
    headers = {'content-type': 'application/json'}
    tmp_list = []
    for i in range (0, num):
        ip = idle_list.pop()
        tmp_list.append(ip)
    for ip in tmp_list:
        url = u'http://%s' % ip
        data = {u'action': u'download',
                u'index': get_task_index(),
                u'interval': 5,
                u'concurrent': concurrent_number
                }
        data = json.dumps(data)
        ret = requests.post(url, data=data, headers=headers)
        print(ret)
        reader_list.append(ip)

def decrease_reader(num):
    headers = {'content-type': 'application/json'}
    tmp_list = []
    for i in range (0, num):
        ip = reader_list.pop()
        tmp_list.append(ip)
    for ip in tmp_list:
        url = u'http://%s' % ip
        data = {u'action': u'stop'}
        data = json.dumps(data)
        ret = requests.post(url, data=data, headers=headers)
        print(ret)
        idle_list.append(ip)

def increase_writer(num):
    headers = {'content-type': 'application/json'}
    tmp_list = []
    for i in range (0, num):
        ip = idle_list.pop()
        tmp_list.append(ip)
    for ip in tmp_list:
        url = u'http://%s' % ip
        data = {u'action': u'upload',
                u'index': get_task_index(),
                u'interval': 5,
                u'concurrent': concurrent_number
                }
        data = json.dumps(data)
        ret = requests.post(url, data=data, headers=headers)
        print(ret)
        writer_list.append(ip)

def decrease_writer(num):
    headers = {'content-type': 'application/json'}
    tmp_list = []
    for i in range (0, num):
        ip = writer_list.pop()
        tmp_list.append(ip)
    for ip in tmp_list:
        url = u'http://%s' % ip
        data = {u'action': u'stop'}
        data = json.dumps(data)
        ret = requests.post(url, data=data, headers=headers)
        print(ret)
        idle_list.append(ip)

largest_list_count = 20
current_list_count = 0
reader_number_list = []
reader_latency_list = []
writer_number_list = []
writer_latency_list = []

def get_reader_latency():
    count = 0
    latency_sum = 0
    for ip in reader_list:
        url = u'http://%s/result' % ip
        try:
            ret = requests.get(url)
            if ret.text != u'no data':
                latency = float(ret.text)
                latency_sum += latency
                count += 1
        except Exception, e:
            print(e)
    if count == 0:
        return 0
    return int(latency_sum / count)

def get_writer_latency():
    count = 0
    latency_sum = 0
    for ip in writer_list:
        url = u'http://%s/result' % ip
        try:
            ret = requests.get(url)
            if ret.text != u'no data':
                latency = float(ret.text)
                latency_sum += latency
                count += 1
        except Exception, e:
            print(e)
    if count == 0:
        return 0
    return int(latency_sum / count)

@app.route(u'/reader_concurrent_number')
def reader_concurrent_number():
    value = concurrent_number * len(reader_list)
    return json.dumps({'value':value})

@app.route(u'/reader_latency')
def reader_latency():
    value = get_reader_latency()
    return json.dumps({'value':value})

@app.route(u'/writer_concurrent_number')
def writer_concurrent_number():
    value = concurrent_number * len(writer_list)
    return json.dumps({'value':value})

@app.route(u'/writer_latency')
def writer_latency():
    value = get_writer_latency()
    return json.dumps({'value':value})

@app.route(u'/', methods=[u'GET', u'POST'])
def index():
    if request.method == u'POST':
        action = request.args.get(u'action')
        if action == u'download':
            reader_number = request.form[u'reader_number']
            print(u'reader_number: %s' % reader_number)
            reader_number = int(reader_number)
            reader_number /= concurrent_number
            current_number = len(reader_list)
            idle_number = len(idle_list)
            if reader_number > idle_number + current_number:
                reader_number = idle_number + current_number
            elif reader_number < 0:
                reader_number = 0
            if reader_number > current_number:
                increase_reader(reader_number - current_number)
            elif reader_number < current_number:
                decrease_reader(current_number - reader_number)
        elif action == u'upload':
            writer_number = request.form[u'writer_number']
            writer_number = int(writer_number)
            writer_number /= concurrent_number
            current_number = len(writer_list)
            idle_number = len(idle_list)
            if writer_number > idle_number + current_number:
                writer_number = idle_number + current_number
            elif writer_number < 0:
                writer_number = 0
            if writer_number > current_number:
                increase_writer(writer_number - current_number)
            elif writer_number < current_number:
                decrease_writer(current_number - writer_number)
        return redirect(url_for(u'index'))
    return render_template(u'index.html')

@app.route(u'/client_info')
def client_info():
    return render_template(u'client_info.html', idle_list=idle_list, reader_list=reader_list, writer_list=writer_list)
if __name__ == u'__main__':
    app.debug = True
    app.run(host=u'0.0.0.0', port=80)
