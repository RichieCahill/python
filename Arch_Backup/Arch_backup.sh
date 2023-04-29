#!/bin/bash

python3 "/usr/local/bin/Arch_backup.py"

host="192.168.99.40"
timeout=300
interval=5

echo "Pinging $host..."

while true; do
	ping -c 1 $host > /dev/null
	if [ $? -eq 0 ]; then
		echo "$host is up."
		break
	else
		echo "$host is down. Waiting $interval seconds..."
		sleep $interval
	fi
	if [ $SECONDS -gt $timeout ]; then
		echo "Timeout reached. $host is still down."
		exit 1
	fi
done

test=$(date +%Y-%m-%d)

chown r2r0m0c0:users "/tmp/etc_$test.tar.zst.encrypted"

runuser -l r2r0m0c0 -c "cp /tmp/etc_$test.tar.zst.encrypted /ZFS/Storage/Backups"

rm "/tmp/etc_$test.tar.zst.encrypted"