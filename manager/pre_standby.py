#! /usr/bin/env python

import sys
import boto.ec2.autoscale
from jinja2 import Template

stack_name = sys.argv[1]
region = sys.argv[2]

conn=boto.ec2.autoscale.connect_to_region(region)

asgs = conn.get_all_groups()

server_name = ServerAutoScalingGroup
client_name = ClientAutoScalingGroup

server_asg = None
client_asg = None
for asg in asgs:
    if stack_name in asg.name and server_name in asg.name:
        server_asg = asg
    if stack_name in asg.name and client_name in asg.name:
        client_asg = asg

assert server_asg
assert client_asg

servers = []
for instance in server_asg.instances:
    servers.append(instance.instance_id)

server_asg_name = server_asg.name

clients = []
for instance in client_asg.instances:
    clients.append(instance.instance_id)

client_asg_name = client_asg.name

with open('do_standby_template.sh') as f:
    template = Template(f.read())

real_script = template.render(servers=servers, server_asg_name=server_asg_name,
                              clients=clients, client_asg_name=client_asg_name,
                              region=region)

with open('do_standby.sh', 'w') as f:
    f.write(real_script)
