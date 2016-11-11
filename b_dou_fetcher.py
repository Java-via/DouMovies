# _*_ coding: utf-8 _*_

import time
import logging
from bs4 import BeautifulSoup
from urllib import request, parse, error
from c_dou_parser import url_parser

logging.basicConfig(level=logging.DEBUG)


def url_fetcher(queue_url, queue_save, bf_url):
    while queue_url.qsize() > 0:
        time.sleep(3)
        print("fetcher is running...", queue_url.qsize())
        classify, url, comment_count, flag = queue_url.get()
        if flag == "base":
            try:
                url = parse.quote(url, safe="%/:=&?~#+!$,;'@()*[]|")
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

                div_movies = soup.find("div", class_="grid-16-8 clearfix").find("div", class_="").find_all("table")
                for item in div_movies:
                    detail_url = item.find_all("td")[0].find("a")["href"]
                    print("get detail url...", [classify, detail_url, comment_count, "detail"])
                    if not bf_url.add(detail_url):
                        queue_url.put([classify, detail_url, comment_count, "detail"])

                next_page = soup.find("div", class_="paginator").find_all("a")[-1].get_text()
                if next_page.strip() == "后页>":
                    classify_next_page = soup.find("div", class_="paginator").find_all("a")[-1]["href"]
                    print("get base url...", [classify, classify_next_page, comment_count, flag])
                    if not bf_url.add(classify_next_page):
                        queue_url.put([classify, classify_next_page, comment_count, flag])
                else:
                    logging.debug("This classify get all movies_url: %s", classify)

            except error.HTTPError as ex:
                logging.error("Url_fetcher error: %s", ex)
        elif flag == "detail":
            url_parser(queue_save, url)
        else:
            logging.error("Url: %s, Unknown flag :%s", url, flag)
    return

# if __name__ == '__main__':
#     classify_item = ['类型:爱情', 'https://movie.douban.com/tag/爱情?start=7840&type=T', '10477121', 'base']
#     url_fetcher(classify_item)
