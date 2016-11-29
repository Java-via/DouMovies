# _*_ coding: utf-8 _*_

# import logging
import requests
from queue import Queue
from urllib import parse
from pybloom import BloomFilter
from bs4 import BeautifulSoup
from z_logcnf import log_init


def get_urls(queue_url, bf_url, req_session, logger):
    logger.debug("get_url is running... %s", queue_url.qsize())
    url = "https://movie.douban.com/tag/"
    resp = req_session.get(url)
    if resp.status_code == 200:
        soup = BeautifulSoup(resp.text, "html5lib")
        tb = soup.find("div", class_="clearfix")
        list_title = [item.get_text().replace("·", "").strip() for item in tb.find_all("a", class_="tag-title-wrapper")]
        list_tags = [item.find_all("td") for item in tb.find_all("tbody")]

        for i in range(len(list_tags)):
            for item in list_tags[i]:
                # 获取url(列表页)  comment(本类总评价数量)  classify(形如 类型：爱情)
                url_classify = parse.urljoin(base="https://movie.douban.com/tag/", url=item.a["href"])
                classify_comment = item.get_text().replace(")", "").split("(")
                item_classify = list_title[i] + ":" + classify_comment[0]
                comment_count = classify_comment[1]
                if not bf_url.add(url_classify):
                    queue_url.put([item_classify, url_classify, comment_count, "base", 3])
    elif resp.status_code == 403:
        logger.warn("Url_init 403: %s, Url is %s", url)
        req_session.cookies.clear()

    logger.debug(queue_url.qsize())
    return queue_url, bf_url

if __name__ == '__main__':
    queue_url = Queue()
    bf_url = BloomFilter(capacity=100000000, error_rate=0.01)
    dict_cookies = {"bid": "Thl_F4uF09U"}
    jar_cookies = requests.utils.cookiejar_from_dict(dict_cookies)
    req_session = requests.Session()
    req_session.cookies = jar_cookies
    logger = log_init("get_url")
    get_urls(queue_url, bf_url, req_session, logger)
