#!/usr/bin/env python

import os
import time
import daemon
import signal
import yaml
import json
import lockfile
import logging
import subprocess

with open(u'%s/client_conf.yaml' % os.path.split(os.path.realpath(__file__))[0], u'r') as f:
    conf = yaml.safe_load(f)

pid_file = conf[u'pid_file']
task_file = conf[u'task_file']
result_file = conf[u'result_file']
raw_result_file = conf[u'raw_result_file']

doing = False
def stop_job(a, b):
    global doing
    try:
        os.remove(task_file)
    except Exception, e:
        logging.warn(u'not find taskfile %s %s' % (task_file, e))
    doing = False
    logging.info(u'stop job')

def start_job(a, b):
    global doing
    if not doing:
        logging.info(u'start job')
        doing = True
    else:
        logging.warn(u'job already running')

def do_job(task_file):
    with open(task_file, u'r') as f:
        data = f.read()
    task = json.loads(data)
    index = task[u'index']
    concurrent = task[u'concurrent']
    action = task[u'action']
    interval = task[u'interval']
    cmd = u'/opt/dynamodb_demo/client/http_load/http_load -p %s -r %s -s %s /opt/dynamodb_demo/client/url/%s_url_%s.txt' % \
        (concurrent, concurrent, interval, action, index)
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    timeout = 2 * int(interval)
    ret = p.wait(timeout=timeout)
    result = p.stdout.readlines()
    with open(raw_result_file, u'w') as f:
        for line in result:
            f.write(line)
    if ret:
        raise Exception(u'ret not zero %s %s' % (ret, result))
    latency = result[4].split(u' ')[1]
    with open(result_file, u'w') as f:
        f.write(latency)
    try:
        p.kill()
    except Exception, e:
        pass

def main_loop():
    logging.basicConfig(filename = u'/tmp/log1.txt', level = logging.INFO)
    pid = os.getpid()
    with open(pid_file,u'w') as f:
        f.write(unicode(pid))
    while True:
        time.sleep(1)
        while os.path.exists(task_file) and doing:
            try:
                do_job(task_file)
            except Exception, e:
                logging.info(u'do_job failed, %s' % e)

ferr = open(u'/tmp/client_daemon.err', u'w+')
context = daemon.DaemonContext(
    stderr=ferr
    )

context.signal_map = {
    signal.SIGUSR1: start_job,
    signal.SIGUSR2: stop_job
    }

with context:
    main_loop()
