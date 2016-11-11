# _*_ coding: utf-8 _*_

import logging
from queue import Queue
from bs4 import BeautifulSoup
from urllib import request, parse, error


def get_urls(queue_url, bf_url):
    list_url_tags = []
    print("get_url is running...", queue_url.qsize())

    url = "https://movie.douban.com/tag/"
    try:
        accept_encoding = "utf-8"
        accept_language = "zh-CN,zh;q=0.8"
        cookie = """ll="108288"; bid=eVWveUvoquI"""
        host = "movie.douban.com"
        user_agent = "Mozilla/5.0 (Windows NT 10.0; WOW64) " \
                     "AppleWebKit/537.36 (KHTML, like Gecko) " \
                     "Chrome/53.0.2785.116 Safari/537.36"

        headers = {"Accept-encoding": accept_encoding,
                   "Accept-language": accept_language,
                   "User-Agent": user_agent,
                   "Cookie": cookie,
                   "Host": host}
        req = request.Request(url=url, data=None, headers=headers)
        resp = request.urlopen(req)
        soup = BeautifulSoup(resp, "html5lib")
        tb = soup.find("div", class_="clearfix")
        list_title = [item.get_text().replace("·", "").strip() for item in tb.find_all("a", class_="tag-title-wrapper")]
        list_tags = [item.find_all("td") for item in tb.find_all("tbody")]

        for i in range(len(list_tags)):
            for item in list_tags[i]:
                url_classify = parse.urljoin(base="https://movie.douban.com/tag/", url=item.a["href"])
                classify_comment = item.get_text().replace(")", "").split("(")
                item_classify = list_title[i] + ":" + classify_comment[0]
                comment_count = classify_comment[1]
                list_url_tags.append([item_classify, url_classify, comment_count, "base"])
                if not bf_url.add(url_classify):
                    queue_url.put([item_classify, url_classify, comment_count, "base"])
    except error.HTTPError as ex:
        logging.error("Get_urls error: %s", ex)
    print(queue_url.qsize())
    return queue_url, bf_url

# if __name__ == '__main__':
#     queue_url = Queue()
#     get_urls(queue_url)
