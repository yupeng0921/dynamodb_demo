#! /bin/bash

function kill_and_exit()
{
	kill -TERM $pid
	exit 0
}

trap "kill_and_exit" INT

while true; do
	/opt/dynamodb_demo/http_load/http_load -p 500 -r 500 -s 5 /tmp/url.txt &
	pid=$!
	wait
	echo ""
done
