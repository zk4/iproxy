#!/bin/bash

count=0
while :; do  
	if test -f "./proxy_down"; then
		make check
		make haproxy
		rm proxy_down
	fi
	sleep 10; 
	count=$(($count + 10)) 
	echo $count
	# if round 1 hour, then run make proxy
	if (( count > 3600 )); then
		count=0
		make get
	fi
done

