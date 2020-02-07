#!/bin/bash
FILE="proxy_down"

if test -f "$FILE"; then
    echo "$FILE exist"
		make proxy
		rm proxy_down
fi
