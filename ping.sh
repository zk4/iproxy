
#!/bin/zsh

PATH=$PATH:/usr/local/bin
PATH=$PATH:/bin
PATH=$PATH:/usr/bin
PATH=$PATH:/Users/zk/anaconda3/bin


RIP=$3
RPT=$4

echo check ...$(date) >/Users/zk/git/pythonPrj/iproxy/check.log

curl --connect-timeout 2 -x "socks5h://$RIP:$RPT" -I https://www.google.com.hk  

if [ $? -eq 0 ]
	 then
	 echo ok $(date) >/Users/zk/git/pythonPrj/iproxy/check.log
	 exit 0
fi

proxy_down=/Users/zk/git/pythonPrj/iproxy/proxy_down
searching=/Users/zk/git/pythonPrj/iproxy/searching
searching_done=/Users/zk/git/pythonPrj/iproxy/searching_done

if test -f "$proxy_down"; then
	if test -f "$searching"; then
		echo searching ...$(date) >>/Users/zk/git/pythonPrj/iproxy/check.log
		exit 1
	else
		touch $searching
		echo start search ...$(date) >>/Users/zk/git/pythonPrj/iproxy/check.log
		source ~/.bash_profile
		cd /Users/zk/git/pythonPrj/iproxy 
		python3 -m iproxy -c ./candidates.txt >>/Users/zk/git/pythonPrj/iproxy/searching.log
		haproxy -f ./haproxy.cfg -p ./haproxy.pid -D -sf `cat ./haproxy.pid`
		touch $searching_done
		rm $searchging
		rm $proxy_down
	fi
else
	touch $proxy_down
fi
exit 1

