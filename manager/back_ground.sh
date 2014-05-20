#! /bin/bash

server_number=$1
client_number=$2

((total_number=server_number+client_number))

while true; do
	num=`salt-key -L | grep 'internal' | wc -l`
	if [ "$num" == "$total_number" ]; then
		break
	fi
	echo "$num $total_number" >> /tmp/background.log
	sleep 1
done

salt-key -A -y

while true; do
	sleep 5
	echo "test" >> /tmp/background.log
done
