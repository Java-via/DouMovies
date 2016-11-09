# _*_ coding: utf-8 _*_

import logging
from bs4 import BeautifulSoup
from urllib import request, parse, error
from c_dou_parser import url_parser

logging.basicConfig(level=logging.DEBUG)


def url_fetcher(queue_url, queue_save):
    while queue_url.qsize() > 0:
        print(queue_url.qsize())
        classify, url, comment_count, flag = queue_url.get()
        if flag == "base":
            try:
                url = parse.quote(url, safe="%/:=&?~#+!$,;'@()*[]|")
                header = {"Accept-encoding": "utf-8"}
                req = request.Request(url=url, headers=header)
                resp = request.urlopen(req)
                soup = BeautifulSoup(resp, "html5lib")

                div_movies = soup.find("div", class_="grid-16-8 clearfix").find("div", class_="").find_all("table")
                for item in div_movies:
                    detail_url = item.find_all("td")[0].find("a")["href"]
                    print([classify, detail_url, comment_count, "detail"])
                    queue_url.put([classify, detail_url, comment_count, "detail"])

                next_page = soup.find("div", class_="paginator").find_all("a")[-1].get_text()
                if next_page.strip() == "后页>":
                    classify_next_page = soup.find("div", class_="paginator").find_all("a")[-1]["href"]
                    print([classify, classify_next_page, comment_count, flag])
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
