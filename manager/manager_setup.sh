#! /bin/bash

echo $* > /tmp/parameters.txt

table_name=$1
region=$2
server_instance_number=$3
client_instance_number=$4
name_db=$5
count_per_user=$6
concurrent_number=$7
url_number=$8

yum install -y nginx
yum install -y python-pip
yum install -y gcc
yum install -y python-devel
pip install flask
pip install uwsgi

cmd="cd /opt/dynamodb_demo/manager; uwsgi --socket 127.0.0.1:3031 --wsgi-file manager.py --callable app --processes 1 --threads 1 --stats 127.0.0.1:9191 -d /opt/dynamodb_demo/uwsgi.log"

echo "$cmd" > run.sh
echo "bash /opt/dynamodb_demo/manage/run.sh" >> /etc/rc.local
bash run.sh

sed -i "s/enabled=0/enabled=1/g" /etc/yum.repos.d/epel.repo

yum install -y salt-master

mkdir -p /srv/salt

service salt-master start
chkconfig salt-master on

sed -i "s/replace_by_table_name/$table_name/g" manager_conf.yaml
sed -i "s/replace_by_region/$region/g" manager_conf.yaml
sed -i "s/replace_by_name_db/$name_db/g" manager_conf.yaml
sed -i "s/replace_by_concurrent_number/$concurrent_number/g" manager_conf.yaml
sed -i "s/replace_by_url_number/$url_number/g" manager_conf.yaml

bash back_ground.sh $server_instance_number $client_instance_number &
