#! /usr/bin/env python

import sys
import time
import json
from jinja2 import Template
import boto
from boto.s3.key import Key
import boto.cloudformation

stack_name = sys.argv[1]
bucket_name = sys.argv[2]
region = sys.argv[3]

conn = boto.cloudformation.connect_to_region(region)

def waiting_stack(status):
    print("before waiting %s" % status)
    while True:
        sts = conn.describe_stacks(stack_name_or_id=stack_name)
        st = sts[0]
        if 'ROLLBACK' in st.stack_status:
            raise Exception(st.stack_status)
        elif st.stack_status == status:
            break
        time.sleep(3)
    print("after waiting %s" % status)

waiting_stack('CREATE_COMPLETE')

parameters = conn.describe_stacks(stack_name_or_id=stack_name)[0].parameters
body = conn.get_template(stack_name_or_id=stack_name)['GetTemplateResponse']['GetTemplateResult']['TemplateBody']
body_dict = json.loads(body)

with open('server_and_client.json') as f:
    template = Template(f.read())

server_instance_number = None
client_instance_number = None
for parameter in parameters:
    if parameter.key == 'ServerInstanceNumber':
        server_instance_number = int(parameter.value)
    elif parameter.key == 'ClientInstanceNumber':
        client_instance_number = int(parameter.value)

assert server_instance_number
assert client_instance_number

servers = []
for i in xrange(server_instance_number):
    servers.append('server%d' % i)

clients = []
for i in xrange(client_instance_number):
    clients.append('client%d' % i)

template_string = template.render(servers=servers, clients=clients)

template_dict = json.loads(template_string)

body_dict['Resources'].update(template_dict)

body_updated = json.dumps(body_dict, indent=4)

with open('/tmp/body_updated.json', 'w') as f:
    f.write(body_updated)

update_template_name = 'update.json'
s3_conn = boto.s3.connect_to_region(region)
b = s3_conn.get_bucket(bucket_name)
k = Key(b)
k.key = update_template_name
k.set_contents_from_string(body_updated)
k.set_acl('public-read')

update_url = 'https://s3-%s.amazonaws.com/%s/%s' % (region, bucket_name, update_template_name)

pn = []
for p in parameters:
    pn.append((p.key,p.value))

conn.update_stack(stack_name, template_url=update_url, parameters=pn)

waiting_stack('UPDATE_COMPLETE')

k.delete()
