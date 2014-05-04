#! /bin/bash

echo $* > /tmp/parameters.txt

yum install -y nginx >> /tmp/setup.log 2>&1
yum install -y python-pip >> /tmp/setup.log 2>&1
yum install -y gcc >> /tmp/setup.log 2>&1
yum install -y python-devel >> /tmp/setup.log 2>&1
pip install flask >> /tmp/setup.log 2>&1
pip install uwsgi >> /tmp/setup.log 2>&1

cp -f client_nginx.conf /etc/nginx/nginx.conf

chkconfig nginx on

echo "cd /opt/dynamodb_demo; uwsgi --socket 127.0.0.1:3031 --wsgi-file client.py --callable app --processes 1 --threads 1 --stats 127.0.0.1:9191 -d /opt/dynamodb_demo/uwsgi.log" >> /etc/rc.local

echo "/opt/dynamodb_demo/client_daemon.py" >> /etc/rc.local
