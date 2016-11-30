# _*_ coding: utf-8 _*_

import requests
from queue import Queue
from threading import Thread
from pybloom import BloomFilter
from z_logcnf import log_init
from a_dou_geturls import get_urls
from d_dou_saver import save_movies
from b_dou_fetcher import url_fetcher
from c_dou_parser import url_parser

if __name__ == '__main__':
    queue_fetch = Queue()
    queue_parse = Queue()
    queue_save = Queue()
    bf_url = BloomFilter(capacity=100000000, error_rate=0.01)

    dict_cookies = {"bid": "Thl_F4uF09U",
                    "__utma": "30149280.479195561.1479796529.1479796529.1480075114.2",
                    "__utmz": "30149280.1479796529.1.1.utmcsr=baidu|utmccn=(organic)|utmcmd=organic",
                    "__utmb": "30149280.0.10.1480075114",
                    "__utmc": "30149280",
                    "_pk_id.100001.4cf6": "a6187c9614309e0a.1480075084.1.1480075133.1480075084.",
                    "_pk_ses.100001.4cf6": "*",
                    "__utma": "223695111.1427633617.1480075114.1480075114.1480075114.1",
                    "__utmb": "223695111.0.10.1480075114",
                    "__utmc": "223695111",
                    "__utmz": "223695111.1480075114.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none)"}
    jar_cookies = requests.utils.cookiejar_from_dict(dict_cookies)
    req_session = requests.Session()
    req_session.cookies = jar_cookies
    requests.packages.urllib3.disable_warnings()   # 关闭requests日志输出

    logger = log_init("logging_dou")
    get_urls(queue_fetch, bf_url, req_session, logger)
    thread_fetch = [Thread(target=url_fetcher, args=(queue_fetch, queue_parse, req_session, logger), name="thread_fetch") for i in range(40)]
    thread_parse = [Thread(target=url_parser, args=(queue_fetch, queue_parse, queue_save, bf_url, logger), name="thread_parse") for i in range(2)]
    thread_save = [Thread(target=save_movies, args=(queue_fetch, queue_parse, queue_save, logger), name="thread_save") for i in range(1)]

    list_threads = list()

    list_threads.extend(thread_fetch)
    list_threads.extend(thread_parse)
    list_threads.extend(thread_save)
    for th in list_threads:
        print(th.name)
        th.setDaemon(1)
        th.start()

    for th in list_threads:
        if th.is_alive():
            print(th.name + " is alive")
            th.join()
    print("the end ...")
    exit()
    # print(queue_url.qsize(), "\t", queue_save.qsize())
    # get_urls(queue_url)
    # print(queue_url.qsize())
    # url_fetcher(queue_url, queue_save)
    # print(queue_url.qsize())
    # print(queue_save.qsize())
    # save_movies(queue_save)
    # print(queue_save.qsize())
