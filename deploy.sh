#! /bin/bash

source conf.sh

aws cloudformation create-stack --stack-name $stack_name --template-body file://template.json --parameters ParameterKey="KeyName",ParameterValue="$key_name" ParameterKey="ResourceLink",ParameterValue="$resource_link" ParameterKey="ReadCapacityUnits",ParameterValue="$read_capacity_units" ParameterKey="WriteCapacityUnits",ParameterValue="$write_capacity_units" ParameterKey="ServerInstanceType",ParameterValue="$server_instance_type" ParameterKey="ClientInstanceType",ParameterValue="$client_instance_type" ParameterKey="ManagerInstanceType",ParameterValue="$manager_instance_type" ParameterKey="ServerInstanceNumber",ParameterValue="$server_instance_number" ParameterKey="ClientInstanceNumber",ParameterValue="$client_instance_number" --region $region