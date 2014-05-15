#! /bin/bash

for ip_addr in $*; do
	scp -i ~/penyu1.pem -r url ec2-user@$ip_addr:/opt/dynamodb_demo/
done
