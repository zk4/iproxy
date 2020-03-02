
#!/bin/zsh

PATH=$PATH:/usr/local/bin
PATH=$PATH:/bin
PATH=$PATH:/usr/bin
PATH=$PATH:/Users/zk/anaconda3/bin

RIP=$3
RPT=$4

echo $(date) "hello" >>ping_only.log
curl --connect-timeout 10 -x "socks5h://$RIP:$RPT" -I https://www.google.com.hk
if [ $? -eq 0 ]
	then
	echo "not down"  >>ping_only.log
	 exit 0
fi
echo "down"  >>ping_only.log
exit 1

