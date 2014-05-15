#! /bin/bash

for ip_addr in $*; do
	scp -i ~/penyu1.pem client* ec2-user@$ip_addr:/opt/dynamodb_demo/
	scp -i ~/penyu1.pem -r static ec2-user@$ip_addr:/opt/dynamodb_demo/
	scp -i ~/penyu1.pem -r templates ec2-user@$ip_addr:/opt/dynamodb_demo/
done
