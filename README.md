## intro
Since a lot of proxy tools there make a proxy. But all of them needs aVPS. If you computer connecting VPS is slow, then you are doomed..
This project works in a trandtional way. Find enough addreees, choose the best one for proxy. and auto reload it by haproxy. 


There are lot of prons by trandtional way:
- You are always swithing proxy address(default every 1 hour), make you being tracked harder.
- You are always using the fatest proxy this tool can ever find.
- It does not matter even using VPS for proxing, only if VPS is the fatest.
-

## config files
`always_test_urls.txt`
put any proxy you think should check every reload round. Something like v2ray, trojan porxy address.

## generaete files
`candidates.txt`
candidate addresses pulled from internet, yet need to check for connectivty from local to google.com.

`google_ok_urls.txt`
addresses have been checked connectivty to google.com

`good_urls.txt`
addresses filtered by speed and by google.com connectivty


`history_urls.txt`
all addresses iproxy have processed.

## usage 
``` bash
make proxy 
	
```
## you can try get list from here,but quality is not good
https://github.com/clarketm/proxy-list

