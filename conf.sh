#! /bin/bash

bucket_name='yupengpublic'
region='ap-northeast-1'
dir_name='dynamodb_demo'
key_name="yupeng"
resource_link="https://s3-us-west-2.amazonaws.com/yupengpublic/dynamodb_demo.zip"
read_capacity_units="1000"
write_capacity_units="1000"
server_instance_type="c3.2xlarge"
client_instance_type="m3.large"
manager_instance_type="t2.small"
server_instance_number="2"
client_instance_number="4"
name_db="name_20K.db"
count_per_user="1"
concurrent_number="500"
url_number="2000"
interval="5"
