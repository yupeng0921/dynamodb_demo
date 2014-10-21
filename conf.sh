#! /bin/bash

bucket_name='yupengtestjenny'
region='ap-northeast-1'
dir_name='dynamodb_demo'
key_name="yupengtest_jenny"
resource_link="https://s3-ap-northeast-1.amazonaws.com/yupengtestjenny/dynamodb_demo.zip"
read_capacity_units="4000"
write_capacity_units="4000"
server_instance_type="c3.2xlarge"
client_instance_type="m3.large"
manager_instance_type="m1.small"
server_instance_number="8"
client_instance_number="16"
name_db="name_20K.db"
count_per_user="1"
concurrent_number="500"
url_number="2000"
interval="5"
