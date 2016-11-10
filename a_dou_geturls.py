# _*_ coding: utf-8 _*_

import logging
from queue import Queue
from bs4 import BeautifulSoup
from urllib import request, parse, error


def get_urls(queue_url):
    list_url_tags = []
    print("get_url is running...", queue_url.qsize())

    url = "https://movie.douban.com/tag/"
    try:
        accept_encoding = "utf-8"
        accept_language = "zh-CN,zh;q=0.8"
        cookie = """ll="108288"; bid=KRgXJ-HZyqg; ap=1; ct=y; _
        pk_ref.100001.4cf6=%5B%22%22%2C%22%22%2C1478765905%2C%22
        https%3A%2F%2Fwww.baidu.com%2Flink%3Furl%3DFxfrUj65Jds79lwLnCNI-7fZRzFXv2YS_m2kdKN4Qm0d
        jOP_HzOoHfQ1PcHYu6tt%26wd%3D%26eqid%3D82773cc90001f0b50000000258242468%22%5D; _
        pk_id.100001.4cf6=c4c0fd1104728cb0.1477665951.13.1478765905.1478763637.;
        _pk_ses.100001.4cf6=*; __utma=30149280.408279850.1477665952.1478691365.1478763631.10;
        __utmb=30149280.4.7.1478764168948; __utmc=30149280;
        __utmz=30149280.1478763631.10.3.utmcsr=baidu|utmccn=(organic)|utmcmd=organic;
        __utma=223695111.1703187677.1477665952.1478763631.1478765905.10; __utmb=223695111.0.10.1478765905;
        __utmc=223695111; __utmz=223695111.1478763631.9.6.utmcsr=baidu|utmccn=(organic)|utmcmd=organic;
        _vwo_uuid_v2=E3DF1C1851C8DCC6D914A081334D0A07|113f38aee5ecb34b708c3639c0c6d4b1"""
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
                queue_url.put([item_classify, url_classify, comment_count, "base"])
    except error.HTTPError as ex:
        logging.error("Get_urls error: %s", ex)
    print(queue_url.qsize())
    return queue_url

if __name__ == '__main__':
    queue_url = Queue()
    get_urls(queue_url)
