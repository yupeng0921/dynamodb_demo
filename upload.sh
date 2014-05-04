#! /bin/bash

source conf.sh

zip -r ../$dir_name.zip ../$dir_name

aws s3 cp ../$dir_name.zip s3://$bucket_name/$dir_name.zip
aws s3api put-object-acl --bucket $bucket_name --key $dir_name.zip --acl public-read
