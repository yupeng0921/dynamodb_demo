#! /bin/bash

bucket_name='yupengpublic'
region='ap-northeast-1'
dir_name='dynamodb_demo'
stack_name="gaming"
key_name="penyu1"
resource_link="https://s3-ap-southeast-1.amazonaws.com/jenny-test/dynamodb_demo.zip"
read_capacity_units="2000"
write_capacity_units="2000"
server_instance_type="c3.2xlarge"
client_instance_type="m3.large"
manager_instance_type="m1.small"
server_instance_number="4"
client_instance_number="8"
name_db="name_20K.db"
count_per_user="10"
concurrent_number="500"
url_number="2000"
interval="5"
