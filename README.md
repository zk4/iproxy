## intro
Since a lot of proxy tools needs a VPS to work. If your computer connecting VPS is slow, then you are doomed..
This project works in a trandtional way and VPS way. Find enough addreesses including your VPS address, choose the best one for proxy. and auto reload it by haproxy.  VPS ensure that you can connect the outer world.

There are lot of prons by trandtional way:
- You are always swithing proxy address, make you being tracked harder.
- You are always using the fastest proxy this tool can ever find.
- Your own VPS is the choice, only if VPS is the fastest.
- Reload haproxy is seamless enough. You won't even notice.
- Health check is quick for recovery.

## config files
`always_test_urls.txt`
put any proxy you think should check every reload round. Something like v2ray, trojan porxy address.

## generaeted files
`candidates.txt`
candidate addresses pulled from internet, yet need to check for connectivty from local to google.com.

`google_ok_urls.txt`
addresses have been checked connectivty to google.com

`good_urls.txt`
addresses filtered by speed and by google.com connectivty


`history_urls.txt`
all addresses iproxy have processed.

`hsitory_good_urls.txt`
addresses used to on good_urls. 

## usage 
``` bash
brew install haproxy
./auto_montior.sh
```

## Todo
- make a ladder by level for address
- incremental enable haproxy 


## Advices
- Don't use load balance proxing web surfing. The slowest speed will probably determine your final speed. That't not we want.
- But if you are downloading by proxy. load blance should be a good mechanism.

## you can try get list from here,but quality is not good
https://github.com/clarketm/proxy-list

