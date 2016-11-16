# _*_ coding: utf-8 _*_

import requests
from queue import Queue
from threading import Thread
from pybloom import BloomFilter
from a_dou_geturls import get_urls
from b_dou_fetcher import url_fetcher
from d_dou_saver import save_movies

if __name__ == '__main__':
    queue_url = Queue()
    queue_save = Queue()
    bf_url = BloomFilter(capacity=100000000, error_rate=0.01)
    req_session = requests.session()
    requests.packages.urllib3.disable_warnings()   # 关闭requests日志输出
    get_urls(queue_url, bf_url, req_session)
    thread_fetch = [Thread(target=url_fetcher, args=(queue_url, queue_save, bf_url, req_session), name="thread_fetch") for i in range(5)]
    thread_save = [Thread(target=save_movies, args=(queue_url, queue_save), name="thread_save") for i in range(2)]

    list_threads = list()

    list_threads.extend(thread_fetch)
    list_threads.extend(thread_save)
    for th in list_threads:
        print(th.name)
        th.setDaemon(1)
        th.start()

    for th in list_threads:
        if th.is_alive():
            print(th.name + " is alive")
            th.join()
    print("1234")
    exit()
    # print(queue_url.qsize(), "\t", queue_save.qsize())
    # get_urls(queue_url)
    # print(queue_url.qsize())
    # url_fetcher(queue_url, queue_save)
    # print(queue_url.qsize())
    # print(queue_save.qsize())
    # save_movies(queue_save)
    # print(queue_save.qsize())
