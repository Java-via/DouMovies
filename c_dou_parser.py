# _*_ coding: utf-8 _*_

import re
import time
import logging
from urllib import parse, request, error
from bs4 import BeautifulSoup
from z_alche import Movie


def url_parser(queue_save, detail_url):
    print(queue_save.qsize())
    try:
        time.sleep(2)
        item_movie = Movie()
        url = parse.quote(detail_url, safe="%/:=&?~#+!$,;'@()*[]|")
        header = {"Accept-encoding": "utf-8"}
        req = request.Request(url=url, headers=header)
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
