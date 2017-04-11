# _*_ coding: utf-8 _*_

import rstr
import random
import requests
from queue import Queue
from threading import Thread
from pybloom import BloomFilter
from z_logcnf import log_init
from a_dou_geturls import get_urls
from d_dou_saver import save_movies
from b_dou_fetcher import url_fetcher
from c_dou_parser import url_parser
from z_alche_movie import BaseModel, engine

USER_AGENT_MOBILE = ["Mozilla/5.0 (Linux; Android 6.0.1; SM-G920V Build/MMB29K) "
                     "AppleWebKit/537.36 (KHTML, like Gecko) "
                     "Chrome/52.0.2743.98 Mobile Safari/537.36",
                     "Mozilla/5.0 (Linux; Android 5.1.1; SM-G928X Build/LMY47X) "
                     "AppleWebKit/537.36 (KHTML, like Gecko) "
                     "Chrome/47.0.2526.83 Mobile Safari/537.36",
                     "Mozilla/5.0 (Windows Phone 10.0; Android 4.2.1; Microsoft; Lumia 950) "
                     "AppleWebKit/537.36 (KHTML, like Gecko) "
                     "Chrome/46.0.2486.0 Mobile Safari/537.36 Edge/13.10586",
                     "Mozilla/5.0 (Linux; Android 6.0.1; Nexus 6P Build/MMB29P) "
                     "AppleWebKit/537.36 (KHTML, like Gecko) "
                     "Chrome/47.0.2526.83 Mobile Safari/537.36",
                     "Mozilla/5.0 (Linux; Android 6.0.1; E6653 Build/32.2.A.0.253) "
                     "AppleWebKit/537.36 (KHTML, like Gecko) "
                     "Chrome/52.0.2743.98 Mobile Safari/537.36",
                     "Mozilla/5.0 (Linux; Android 6.0; HTC One M9 Build/MRA58K) "
                     "AppleWebKit/537.36 (KHTML, like Gecko) "
                     "Chrome/52.0.2743.98 Mobile Safari/537.36",
                     ]

USER_AGENT_PC = ["Mozilla/5.0 (Linux; Android 7.0; Pixel C Build/NRD90M; wv) "
                 "AppleWebKit/537.36 (KHTML, like Gecko) "
                 "Version/4.0 Chrome/52.0.2743.98 Safari/537.36",
                 "Mozilla/5.0 (Linux; Android 6.0.1; SGP771 Build/32.2.A.0.253; wv) "
                 "AppleWebKit/537.36 (KHTML, like Gecko) "
                 "Version/4.0 Chrome/52.0.2743.98 Safari/537.36",
                 "Mozilla/5.0 (Linux; Android 5.1.1; SHIELD Tablet Build/LMY48C) "
                 "AppleWebKit/537.36 (KHTML, like Gecko) "
                 "Chrome/52.0.2743.98 Safari/537.36",
                 "Mozilla/5.0 (Linux; Android 5.0.2; SAMSUNG SM-T550 Build/LRX22G) "
                 "AppleWebKit/537.36 (KHTML, like Gecko) "
                 "SamsungBrowser/3.3 Chrome/38.0.2125.102 Safari/537.36",
                 "Mozilla/5.0 (Linux; Android 4.4.3; KFTHWI Build/KTU84M) "
                 "AppleWebKit/537.36 (KHTML, like Gecko) "
                 "Silk/47.1.79 like Chrome/47.0.2526.80 Safari/537.36",
                 "Mozilla/5.0 (Linux; Android 5.0.2; LG-V410/V41020c Build/LRX22G) "
                 "AppleWebKit/537.36 (KHTML, like Gecko) "
                 "Version/4.0 Chrome/34.0.1847.118 Safari/537.36"]

RANDOM_USER_AGENT = [random.choice(USER_AGENT_MOBILE), random.choice(USER_AGENT_PC)]

ACCEPT = "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"
ACCEPT_ENCODING = "gzip, deflate, sdch, br"

BID = rstr.xeger(r"[A-Z]{2}[a-z][0-9]{3}[A-Z]{3}[a-z][A-Z]")

if __name__ == '__main__':
    BaseModel.metadata.create_all(engine)

    queue_fetch = Queue()
    queue_parse = Queue()
    queue_save = Queue()
    bf_url = BloomFilter(capacity=100000000, error_rate=0.01)

    dict_cookies = {"bid": BID}
    jar_cookies = requests.utils.cookiejar_from_dict(dict_cookies)
    req_session = requests.Session()
    req_session.cookies = jar_cookies
    header = {
        "User-Agent": random.choice(RANDOM_USER_AGENT),
        "Accept": ACCEPT,
        "Accept-Encoding": ACCEPT_ENCODING
    }
    req_session.headers = header
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
