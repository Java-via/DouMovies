# _*_ coding: utf-8 _*_

import logging
import requests
from pybloom import BloomFilter
from queue import Queue
from bs4 import BeautifulSoup
from urllib import parse


def get_urls(queue_url, bf_url, req_session):
    try:
        print("get_url is running...", queue_url.qsize())

        url = "https://movie.douban.com/tag/"
        resp = req_session.get(url)

        soup = BeautifulSoup(resp.text, "html5lib")
        tb = soup.find("div", class_="clearfix")
        list_title = [item.get_text().replace("·", "").strip() for item in tb.find_all("a", class_="tag-title-wrapper")]
        list_tags = [item.find_all("td") for item in tb.find_all("tbody")]

        for i in range(len(list_tags)):
            for item in list_tags[i]:
                url_classify = parse.urljoin(base="https://movie.douban.com/tag/", url=item.a["href"])
                classify_comment = item.get_text().replace(")", "").split("(")
                item_classify = list_title[i] + ":" + classify_comment[0]
                comment_count = classify_comment[1]
                if not bf_url.add(url_classify):
                    queue_url.put([item_classify, url_classify, comment_count, "base", 3])
    except requests.HTTPError as ex:
        req_session.cookies.clear_session_cookies()
        print(ex)

    print(queue_url.qsize())
    return queue_url, bf_url

if __name__ == '__main__':
    queue_url = Queue()
    bf_url = BloomFilter(capacity=100000000, error_rate=0.01)
    req_session = requests.Session()
    get_urls(queue_url, bf_url, req_session)
