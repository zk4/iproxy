#!/bin/zsh

PATH=$PATH:/usr/local/bin
PATH=$PATH:/bin
PATH=$PATH:/usr/bin
PATH=$PATH:/Users/zk/anaconda3/bin


RIP=$3
RPT=$4

curl -x "socks5h://$RIP:$RPT" -I "https://www.google.com"  &> /Users/zk/git/pythonPrj/iproxy/check.log

if [ $? -eq 0 ]
	then
	 exit 0
fi

touch /Users/zk/git/pythonPrj/iproxy/proxy_down
exit 1

