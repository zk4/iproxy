#coding: utf-8
import requests
from concurrent.futures import ThreadPoolExecutor
from .logx import setup_logging
from .logx.color import color  
import time
import sys
import argparse
import logging
setup_logging()
logger = logging.getLogger(__name__)

def check(proxyUrl,targetUrl="http://www.google.com"):
    proxyUrl = proxyUrl.strip()
    proxies = { "https":proxyUrl ,"http": proxyUrl}

    r = requests.get(targetUrl,proxies = proxies,timeout=5)
    if r.status_code == 200:
        logger.debug("%s" % proxyUrl)
        write('good.txt',proxyUrl)
        return True
    return False


def write(localfile,line):
    with open(localfile,"+a") as f:
        f.write(line+"\n")

def lines(localfile):
    with open(localfile) as f:
        for line in f:
            yield line

def speedTest(proxyUrl,url) :
    proxyUrl = proxyUrl.strip()
    logger.debug(f'speed test... {proxyUrl}           ')
    start = time.time()
    proxies = { "https":proxyUrl ,"http": proxyUrl}
    r = requests.get(url,proxies=proxies, stream=True)
    total_length = r.headers.get('content-length')
    dl = 0
    if total_length is None: # no content length header
        logger.debug(f'no content-length')
    else:
        total_length = int(total_length)
        if total_length  != 104857600:
             logger.debug(f'content length is too small')
             return 
        logger.debug(f'content lenght is {total_length}')
        lowerSpeedTimesMax = 300
        lowerSpeedLimit = 100
        lowerSpeedTimes = 0
        testLengthPercentage = 0.02
        
        for chunk in r.iter_content(1024):
            dl += len(chunk)
            done = int(50 * dl / total_length)
            if (dl / total_length) > testLengthPercentage:
                break
            speed = dl/1024//(time.time() - start)
            logger.debug("[%s%s] %s k/bps" % ('=' * done, ' ' * (50-done),speed ))
            logger.debug("%s: %s k/bps" % (proxyUrl,speed))
            if speed < lowerSpeedLimit:
                lowerSpeedTimes+=1
                if lowerSpeedTimes > lowerSpeedTimesMax:
                    logger.debug(f'too slow {proxyUrl}')
                    return
            else:
                lowerSpeedTimes=0
        logger.info(f'good! {speed} {proxyUrl}')



def combine(proxyUrl):
    on = check(proxyUrl)
    if on:
        try:
            speedTest(proxyUrl,"http://hnd-jp-ping.vultr.com/vultr.com.100MB.bin")
        except Exception as e:
            # logger.exception(e)
            pass
import sys

def feed(count):
    print("-------------",count)
    return count * 2

def main(args):
    with ThreadPoolExecutor(max_workers=10) as executor:
        for proxyUrl in lines("./candidates.txt"):
            executor.submit(combine,proxyUrl)

def entry_point():
    parser = createParse()
    mainArgs=parser.parse_args()
    main(mainArgs)


def createParse():
    print(color.R+"Don`t use public proxy to access private data when SSL invalidated! MITM is comming!"+color.W)
    parser = argparse.ArgumentParser( formatter_class=argparse.ArgumentDefaultsHelpFormatter, description="")
    # subparsers = parser.add_subparsers()
    # eat_parser = subparsers.add_parser('eat',formatter_class=argparse.ArgumentDefaultsHelpFormatter, description="",  help='sub command demo')
    # eat_parser.add_argument('-c', '--count',type=int,required=False, help='carrots count', default="")  

    return parser
