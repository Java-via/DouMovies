# _*_ coding: utf-8 _*_

import logging
from bs4 import BeautifulSoup
from urllib import request, parse, error


def get_urls(queue_url):
    list_url_tags = []
    print(queue_url.qsize())

    url = "https://movie.douban.com/tag/"
    try:
        resp = request.urlopen(url)
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
                queue_url.put([item_classify, url_classify, comment_count, "base"])
    except error.HTTPError as ex:
        logging.error("Get_urls error: %s", ex)
    print(queue_url.qsize())
    return queue_url

# if __name__ == '__main__':
#     get_urls(queue_url)
