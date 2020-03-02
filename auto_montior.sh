#!/bin/bash

count=0
# start lb first to access web as quick as possiable
make haproxy_lb
# then no matter what,get the newest list, and choose the fatest one
make proxy

while :; do  
	echo $count
	if test -f "./proxy_down"; then
		# temparay swith to loadblance
		make haproxy_lb
		# don`t search, just use the cache 
		make check
		make haproxy
		rm proxy_down
	fi
	sleep 10; 
	count=$(($count + 10)) 
	# if round 1 hour, then run make proxy
	if (( count > 3600 )); then
		count=0
		make get
	fi
done

