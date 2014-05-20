#! /bin/bash

echo $* > /tmp/parameters.txt

manager_ip=$1

yum install -y nginx
yum install -y python-pip
yum install -y gcc
yum install -y python-devel
pip install flask
pip install uwsgi

cp -f client_nginx.conf /etc/nginx/nginx.conf

service nginx start
chkconfig nginx on

cmd="cd /opt/dynamodb_demo/client; uwsgi --socket 127.0.0.1:3031 --wsgi-file client.py --callable app --processes 1 --threads 1 --stats 127.0.0.1:9191 -d /opt/dynamodb_demo/uwsgi.log"

echo "$cmd" >> /etc/rc.local
echo "$cmd" > /tmp/run.sh
bash /tmp/run.sh

cmd="/opt/dynamodb_demo/client/client_daemon.py"
echo "$cmd" >> /etc/rc.local
echo "$cmd" > /tmp/run.sh
bash /tmp/run.sh

sed -i "s/enabled=0/enabled=1/g" /etc/yum.repos.d/epel.repo

yum install -y salt-minion >> /tmp/setup.log 2>&1

sed -i "s/replace_by_manager_ip/$manager_ip/g" minion
cp minion /etc/salt/minion

service salt-minion start
chkconfig salt-minion on
