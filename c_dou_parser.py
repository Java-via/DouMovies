# _*_ coding: utf-8 _*_

import re
import time
import logging
from urllib import parse, request, error
from bs4 import BeautifulSoup
from z_alche import Movie


def url_parser(queue_save, detail_url):
    print("parser is running...", queue_save.qsize())
    try:
        time.sleep(3)
        item_movie = Movie()
        url = parse.quote(detail_url, safe="%/:=&?~#+!$,;'@()*[]|")
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
        content = soup.find("div", id="content")
        article = soup.find("div", class_="article")
        mainpic = article.find("div", id="mainpic")
        dou_score = article.find("div", class_="rating_wrap clearbox")
        dou_beterthan = article.find("div", class_="rating_betterthan")
        info = article.find("div", id="info").get_text()
        list_info = []

        list_score = [item.get_text() for item in dou_score.find_all("span")[1::2]]
        str_starpercent = re.sub(pattern="[\[\]'\s]", repl="", string=str(list_score))

        item_movie.score = dou_score.find("strong").get_text()
        list_starpercent = str_starpercent.split(",")
        item_movie.comment, *star_percent = list_starpercent
        item_movie.star_percent = re.sub(pattern="[\[\]']", repl="", string=str(star_percent))
        item_movie.better_than = re.sub(r"[\s]", "", (dou_beterthan.get_text().strip().replace("\n", ","))) if dou_beterthan else ""

        for line in info.split("\n"):
            if line.find(":") > 0:
                list_info.append(line.strip())
        dict_info = {}
        for item in list_info:
            dict_info[item.split(":")[0]] = item.split(":")[1].strip()

        director = dict_info.get("导演")
        screenwriter = dict_info.get("编剧")
        performer = dict_info.get("主演")

        genre = dict_info.get("类型")
        country = dict_info.get("制片国家/地区")
        language = dict_info.get("语言")

        release_time = dict_info.get("上映日期")
        length = dict_info.get("片长")
        another_name = dict_info.get("又名")
        imdb = dict_info.get("IMDb链接")

        item_movie.url = url
        item_movie.img_url = mainpic.find("a").find("img").get("src")
        item_movie.name, item_movie.year = [item.get_text() for item in content.find("h1").find_all("span")]

        item_movie.director = director if director else ""
        item_movie.screenwriter = screenwriter if screenwriter else ""
        item_movie.performer = performer if performer else ""

        item_movie.genre = genre if genre else ""
        item_movie.country = country if country else ""
        item_movie.language = language if language else ""

        item_movie.release_time = release_time if release_time else ""
        item_movie.length = length if length else ""
        item_movie.another_name = another_name if another_name else ""
        item_movie.imdb = imdb if imdb else ""

        # print(item_movie.url, item_movie.img_url, item_movie.name, item_movie.year,
        #       item_movie.director, item_movie.screenwriter, item_movie.performer,
        #       item_movie.genre, item_movie.country, item_movie.language,
        #       item_movie.release_time, item_movie.length, item_movie.another_name,
        #       item_movie.better_than, item_movie.imdb)
        queue_save.put(item_movie)
        # save_movies(item_movie)
    except error.HTTPError as ex:
        logging.error("Url_fetcher error: %s", ex)
    return queue_save

# if __name__ == '__main__':
#     get_detail("https://movie.douban.com/subject/26340522/")
