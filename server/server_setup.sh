#! /bin/bash

echo $* >> /tmp/parameters.txt

manager_ip=$1
table_name=$2
region=$3
stack_name=$4

yum install -y perl-libwww-perl # for GET command
instance_id=`GET 169.254.169.254/latest/meta-data/instance-id`
instance_name="$stack_name""_server"
/usr/bin/aws ec2 create-tags --resources $instance_id --tags Key=Name,Value=$instance_name --region $region

yum install -y nginx
yum install -y python-pip
yum install -y gcc
yum install -y python-devel
pip install flask
pip install uwsgi

sed -i "s/replace_by_region/$region/g" server_conf.yaml
sed -i "s/replace_by_table_name/$table_name/g" server_conf.yaml

cp -f server_nginx.conf /etc/nginx/nginx.conf
cp -f 90-nproc.conf /etc/security/limits.d/

service nginx start
chkconfig nginx on

ec2_uid=`awk 'BEGIN {FS=":"} {if($1=="ec2-user")print $3}' /etc/passwd`

cmd="ulimit -n 65536; cd /opt/dynamodb_demo/server; uwsgi --socket 127.0.0.1:3031 --wsgi-file server.py --callable app --processes 8 --threads 512 --stats 127.0.0.1:9191 --uid $ec2_uid -d /opt/dynamodb_demo/uwsgi.log -L --cpu-affinity 1"

echo "$cmd" >> /etc/rc.local

echo "$cmd" > /tmp/run.sh
bash /tmp/run.sh

sed -i "s/enabled=0/enabled=1/g" /etc/yum.repos.d/epel.repo

yum install -y salt-minion

sed -i "s/replace_by_manager_ip/$manager_ip/g" minion
cp minion /etc/salt/minion

service salt-minion start
chkconfig salt-minion on
