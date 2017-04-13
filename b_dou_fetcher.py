# _*_ coding: utf-8 _*_

import time
import random
import string
import requests
from bs4 import BeautifulSoup


def url_fetcher(queue_fetch, queue_parse, req_session, logger):
    from h_doumovies import RANDOM_USER_AGENT, BID
    while queue_fetch.qsize() > 0:
        time.sleep(10)
        dict_cookies = {"bid": BID}
        jar_cookies = requests.utils.cookiejar_from_dict(dict_cookies)
        req_session.cookies = jar_cookies
        req_session.headers.update({
            "User-Agent": random.choice(RANDOM_USER_AGENT)
        })
        logger.debug("fetcher is running... %s, %s", queue_fetch.qsize(), queue_parse.qsize())
        list_url_info = queue_fetch.get()
        classify, url, comment_count, flag, repeat = list_url_info
        try:
            # url = parse.quote(url, safe="%/:=&?~#+!$,;'@()*[]|")
            resp = req_session.get(url)
            if len(resp.text) > 200:
                soup = BeautifulSoup(resp.text, "html5lib")
                queue_parse.put([classify, (url, soup), comment_count, flag, repeat])
                logger.debug("fetcher is running...add to parse %s, %s", queue_fetch.qsize(), queue_parse.qsize())
            else:
                logger.warn("Url_fetcher 403: %s, Url is %s", url)
                dict_cookies = {"bid": "".join(random.sample(string.ascii_letters + string.digits, 11))}
                jar_cookies = requests.utils.cookiejar_from_dict(dict_cookies)
                req_session = requests.Session()
                req_session.cookies = jar_cookies
                logger.warn("clear cookies finish: %s", requests.utils.dict_from_cookiejar(req_session.cookies))
                queue_fetch.put(classify, url, comment_count, flag, repeat)
        except requests.HTTPError as ex:
            if repeat >= 0:
                repeat -= 1
                queue_fetch.put(classify, url, comment_count, flag, repeat)
            logger.error("Url_fetcher error: %s, Url is %s", ex, url)
        except Exception as exce:
            logger.error("Url_fetcher Error is %s, Url is %s", exce, url)
    return

# if __name__ == '__main__':
#     classify_item = ['类型:爱情', 'https://movie.douban.com/tag/爱情?start=7840&type=T', '10477121', 'base', 3]
#     queue_fetch = Queue()
#     queue_parse = Queue()
#     dict_cookies = {"bid": "".join(random.sample(string.ascii_letters + string.digits, 11))}
#     jar_cookies = requests.utils.cookiejar_from_dict(dict_cookies)
#     req_session = requests.Session()
#     req_session.cookies = jar_cookies
#     logger = log_init("fetcher")
#     queue_fetch.put(classify_item)
#     print(queue_fetch.qsize())
#     print(queue_parse.qsize())
#     url_fetcher(queue_fetch, queue_parse, req_session, logger)
#     print(queue_fetch.qsize())
#     print(queue_parse.qsize())
