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

    dict_cookies = {"bid": "6XeB4bwmsH0"}
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
