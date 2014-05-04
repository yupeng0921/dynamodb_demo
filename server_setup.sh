#! /bin/bash

echo $* >> /tmp/parameters.txt

manager_ip=$1
table_name=$2
region=$3
yum install -y nginx >> /tmp/setup.log 2>&1
yum install -y python-pip >> /tmp/setup.log 2>&1
yum install -y gcc >> /tmp/setup.log 2>&1
yum install -y python-devel >> /tmp/setup.log 2>&1
pip install flask >> /tmp/setup.log 2>&1
pip install uwsgi >> /tmp/setup.log 2>&1

sed -i "s/server_region/$region/g" server_conf.yaml
sed -i "s/server_table_name/$table_name/g" server_conf.yaml

cp -f server_nginx.conf /etc/nginx/nginx.conf
cp -f 90-nproc.conf /etc/security/limits.d/

chkconfig nginx on

ec2_uid=`awk 'BEGIN {FS=":"} {if($1=="ec2-user")print $3}' /etc/passwd`

echo "ulimit -n 65536; cd /opt/dynamodb_demo; uwsgi --socket 127.0.0.1:3031 --wsgi-file server.py --callable app --processes 8 --threads 1024 --stats 127.0.0.1:9191 --uid $ec2_uid -d /opt/dynamodb_demo/uwsgi.log" >> /etc/rc.local
