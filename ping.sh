
#!/bin/zsh

PATH=$PATH:/usr/local/bin
PATH=$PATH:/bin
PATH=$PATH:/usr/bin
PATH=$PATH:/Users/zk/anaconda3/bin


RIP=$3
RPT=$4

proxy_down=/Users/zk/git/pythonPrj/iproxy/proxy_down
echo check ...$(date) >/Users/zk/git/pythonPrj/iproxy/check.log

curl --connect-timeout 3 -x "socks5h://$RIP:$RPT" -I https://www.google.com.hk  

if [ $? -eq 0 ]
	 then
	 echo ok $(date) >/Users/zk/git/pythonPrj/iproxy/check.log
	 rm $proxy_down
	 exit 0
fi

touch $proxy_down
exit 1

