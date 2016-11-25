# _*_ coding: utf-8 _*_

import time
# import logging
import requests
from queue import Queue
from urllib import parse
from bs4 import BeautifulSoup
from pybloom import BloomFilter
from c_dou_parser import url_parser
from z_logcnf import log_init


def url_fetcher(queue_url, queue_save, bf_url, req_session, logger):
    while queue_url.qsize() > 0:
        time.sleep(3)
        logger.debug("fetcher is running... %s", queue_url.qsize())
        list_url_info = queue_url.get()
        classify, url, comment_count, flag, repeat = list_url_info
        if flag == "base":
            try:
                # url = parse.quote(url, safe="%/:=&?~#+!$,;'@()*[]|")
                resp = req_session.get(url)
                soup = BeautifulSoup(resp.text, "html5lib")

                div_movies = soup.find("div", class_="grid-16-8 clearfix").find("div", class_="").find_all("table")
                for item in div_movies:
                    detail_url = parse.urljoin(base="https://movie.douban.com/tag/", url=item.find_all("td")[0].find("a")["href"])
                    logger.debug("get detail url...%s, %s, %s, %s, %s", classify, detail_url, comment_count, "detail", 2)
                    if not bf_url.add(detail_url):
                        queue_url.put([classify, detail_url, comment_count, "detail", 2])

                next_page = soup.find("div", class_="paginator").find_all("a")[-1].get_text()
                if next_page.strip() == "后页>":
                    classify_next_page = soup.find("div", class_="paginator").find_all("a")[-1]["href"]
                    logger.debug("get base url...%s, %s, %s, %s, %s", classify, classify_next_page, comment_count, flag, 3)
                    if not bf_url.add(classify_next_page):
                        queue_url.put([classify, classify_next_page, comment_count, flag, 3])
                else:
                    logger.debug("This classify get all movies_url: %s", classify)
            except requests.HTTPError as ex:
                req_session.cookies.clear_session_cookies()
                if repeat >= 0:
                    repeat -= 1
                    queue_url.put(classify, url, comment_count, flag, repeat)
                logger.error("Url_fetcher error: %s, Url is %s", ex, url)
            except Exception as exce:
                logger.error("Error is %s, Url is %s", exce, url)
        elif flag == "detail":
            url_parser(queue_url, queue_save, list_url_info, req_session, logger)
        else:
            logger.error("Url: %s, Unknown flag :%s", url, flag)
    return

if __name__ == '__main__':
    classify_item = ['类型:爱情', 'https://movie.douban.com/tag/爱情?start=7840&type=T', '10477121', 'base', 3]
    queue_url = Queue()
    queue_save = Queue()
    bf_url = BloomFilter(capacity=100000000, error_rate=0.01)
    req_session = requests.session()
    logger = log_init("fetcher")
    queue_url.put(classify_item)
    url_fetcher(queue_url, queue_save, bf_url, req_session, logger)
