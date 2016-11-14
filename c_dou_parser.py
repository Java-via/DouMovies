# _*_ coding: utf-8 _*_

import re
import time
import logging
from queue import Queue
from urllib import parse, request, error
from bs4 import BeautifulSoup
from z_alche_movie import Movie


def url_parser(queue_url, queue_save, list_url_info):
    classify, detail_url, comment_count, flag, repeat = list_url_info
    print("parser is running...", queue_save.qsize())
    time.sleep(3)
    item_movie = Movie()
    url = parse.quote(detail_url, safe="%/:=&?~#+!$,;'@()*[]|")
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
        content = soup.find("div", id="content")
        article = soup.find("div", class_="article")
        mainpic = article.find("div", id="mainpic")

        img_url = mainpic.find("a").find("img").get("src")
        name, year = [item.get_text() for item in content.find("h1").find_all("span")]

        dou_score = article.find("div", class_="rating_wrap clearbox")
        dou_beterthan = article.find("div", class_="rating_betterthan")
        info = article.find("div", id="info").get_text()
        list_info = []

        list_score = [item.get_text() for item in dou_score.find_all("span")[1::2]]
        str_starpercent = re.sub(pattern="[\[\]'\s]", repl="", string=str(list_score))

        score = dou_score.find("strong").get_text()
        list_starpercent = str_starpercent.split(",")
        comment, *star_percent = list_starpercent
        star_percent = re.sub(pattern="[\[\]']", repl="", string=str(star_percent))
        better_than = re.sub(r"[\s]", "", (dou_beterthan.get_text().strip().replace("\n", ","))) if dou_beterthan else ""

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
        item_movie.img_url = img_url if img_url else ""
        item_movie.name = name if name else ""
        item_movie.year = year if year else ""

        item_movie.director = director if director else ""
        item_movie.screenwriter = screenwriter if screenwriter else ""
        item_movie.performer = performer if performer else ""

        item_movie.genre = genre if genre else ""
        item_movie.country = country if country else ""
        item_movie.language = language if language else ""

        item_movie.release_time = release_time if release_time else ""
        item_movie.length = length if length else ""
        item_movie.another_name = another_name if another_name else ""

        item_movie.score = score if score else -1
        item_movie.comment = comment if comment else -1
        item_movie.comment_this_classify = comment_count if comment_count else -1

        item_movie.star_percent = star_percent if star_percent else ""
        item_movie.better_than = better_than if better_than else ""
        item_movie.imdb = imdb if imdb else ""

        # print(item_movie.url, item_movie.img_url, item_movie.name, item_movie.year,
        #       item_movie.director, item_movie.screenwriter, item_movie.performer,
        #       item_movie.genre, item_movie.country, item_movie.language,
        #       item_movie.release_time, item_movie.length, item_movie.another_name,
        #       item_movie.better_than, item_movie.imdb)
        queue_save.put(item_movie)
        # save_movies(item_movie)
    except error.HTTPError as http_ex:
        if repeat >= 0:
            repeat -= 1
            queue_url.put(list_url_info)
        logging.error("Url_parser error: %s, Url is %s", http_ex, url)
    except Exception as ex:
        logging.error("Url_parser error: %s, Url is %s", ex, url)
    return queue_save

if __name__ == '__main__':
    queue_url = Queue()
    queue_save = Queue()
    list_url_info = ['类型:爱情', 'https://movie.douban.com/subject/2173246/', '10477121', 'detail', 2]
    url_parser(queue_url, queue_save, list_url_info)
