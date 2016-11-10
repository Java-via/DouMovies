# _*_ coding: utf-8 _*_

import time
import logging
from bs4 import BeautifulSoup
from urllib import request, parse, error
from c_dou_parser import url_parser

logging.basicConfig(level=logging.DEBUG)


def url_fetcher(queue_url, queue_save):
    while queue_url.qsize() > 0:
        time.sleep(3)
        print("fetcher is running...", queue_url.qsize())
        classify, url, comment_count, flag = queue_url.get()
        if flag == "base":
            try:
                url = parse.quote(url, safe="%/:=&?~#+!$,;'@()*[]|")
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

                div_movies = soup.find("div", class_="grid-16-8 clearfix").find("div", class_="").find_all("table")
                for item in div_movies:
                    detail_url = item.find_all("td")[0].find("a")["href"]
                    print("get detail url...", [classify, detail_url, comment_count, "detail"])
                    queue_url.put([classify, detail_url, comment_count, "detail"])

                next_page = soup.find("div", class_="paginator").find_all("a")[-1].get_text()
                if next_page.strip() == "后页>":
                    classify_next_page = soup.find("div", class_="paginator").find_all("a")[-1]["href"]
                    print("get base url...", [classify, classify_next_page, comment_count, flag])
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
