#coding: utf-8
import requests
from concurrent.futures import ThreadPoolExecutor
from .logx import setup_logging
from .logx.color import color  
from .get_candidates import main as get_candidates
import time
import sys
import os
import threading
import argparse
import logging
setup_logging()
logger = logging.getLogger(__name__)

# for use
good_urls= set()

google_ok_urls= set()

# saved all history_urls 
history_urls = set() 

def check(proxyUrl,targetUrl="http://www.google.com"):
    proxyUrl = proxyUrl.strip()
    logger.info(f'check {proxyUrl}')
    proxyUrl = proxyUrl.strip()
    proxies = { "https":proxyUrl ,"http": proxyUrl}

    r = requests.get(targetUrl,proxies = proxies,timeout=3)
    if r.status_code == 200:
        logger.debug("google ok: %s" % proxyUrl)
        google_ok_urls.add(proxyUrl)
        return True
    return False

def backup(proxyUrl):
    with open("./good_urls.txt",'w') as f:
        for line in good_urls:
            f.write(line+"\n")
    with open("./google_ok_urls.txt",'w') as f:
        for line in google_ok_urls:
            f.write(line+"\n")
    with open("./history_urls.txt",'w') as f:
        for line in history_urls:
            f.write(line)



def candidate(filename):
    if os.path.exists(filename):
        with open(filename) as f:
            for line in f:
                yield line

def candidates(all_candidates=False):
    yield from candidate("./google_ok_urls.txt")
    yield from candidate("./good_urls.txt")
    yield from candidate("./candidates.txt")
    if all_candidates:
        yield from candidate("./history_urls.txt")


def speedTest(proxyUrl,url) :
    proxyUrl = proxyUrl.strip()
    logger.debug(f'speed: {proxyUrl}          ')
    start = time.time()
    proxies = { "https":proxyUrl ,"http": proxyUrl}
    r = requests.get(url,proxies=proxies, stream=True,timeout=5)
    total_length = r.headers.get('content-length')
    dl = 0
    if total_length is None: # no content length header
        logger.debug(f'no content-length')
    else:
        total_length = int(total_length)
        if total_length  != 104857600:
             logger.debug(f'content length is too small {proxyUrl}')
             return 
        logger.debug(f'content lenght is {total_length}')
        lowerSpeedTimesMax = 50
        lowerSpeedLimit = 10
        lowerSpeedTimes = 0
        testLengthPercentage = 0.005
        
        for chunk in r.iter_content(1024):
            dl += len(chunk)
            if (dl / total_length) > testLengthPercentage:
                break
            speed = dl/1024//(time.time() - start)
            logger.debug("%s: %s kb/s" % (proxyUrl,speed))
            if speed < lowerSpeedLimit:
                lowerSpeedTimes+=1
                if lowerSpeedTimes > lowerSpeedTimesMax:
                    logger.debug(f'slow {speed} kb/s {proxyUrl}')
                    return
            else:
                lowerSpeedTimes=0
        logger.info(f'good! {speed} kb/s {proxyUrl}')
        good_urls.add(proxyUrl)



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

    if args.get_candidates:
        get_candidates()
        return

    if args.check_file:
        no_duplicates = set()
        with ThreadPoolExecutor(max_workers=100) as executor:
            for proxyUrl in candidates(args.all_candidates):
                if proxyUrl not in no_duplicates:
                    history_urls.add(proxyUrl)
                    no_duplicates.add(proxyUrl)
                    executor.submit(combine,proxyUrl)

        executor.shutdown()
        backup("./good_urls.txt")
        print("end ..")




def entry_point():
    parser = createParse()
    mainArgs=parser.parse_args()
    main(mainArgs)


def createParse():
    print(color.R+"WARNNING:Proxy is checked for certification validation. Don`t use public proxy to access private data when SSL invalidated! You may under MITM attack if so!"+color.W)
    parser = argparse.ArgumentParser( formatter_class=argparse.ArgumentDefaultsHelpFormatter, description="")
    parser.add_argument('-c', '--check_file',type=str,required=False, help='local candidates file, content format schema://ip:port', default="./candidates.txt")  
    parser.add_argument('-g', '--get_candidates', action='store_true', help='candidates web sites, content format schema://ip:port')  
    parser.add_argument('-a', '--all_candidates', action='store_true',default=False, help='if test all candidates in history_urls.txt')  

    return parser
