# _*_ coding: utf-8 _*_

import re
import json
import logging
import sqlalchemy
from queue import Queue
from bs4 import BeautifulSoup
from sqlalchemy.orm import sessionmaker
from urllib import request, parse, error
from z_alche import *

queue_url = Queue()


def get_urls():
    list_url_tags = []

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
                while True:
                    url_more = url_classify + "?start=" + str(i) + "type=T"
                queue_url.put([item_classify, url_classify, comment_count, "base"])
    except error.HTTPError as ex:
        logging.error("Get_urls error: %s", ex)


def url_fetcher(classify_item):
    classify, url, comment_count, flag = classify_item
    if flag == "base":
        try:
            url = parse.quote(url, safe="%/:=&?~#+!$,;'@()*[]|")
            header = {"Accept-encoding": "utf-8"}
            req = request.Request(url=url, headers=header)
            resp = request.urlopen(req)
            soup = BeautifulSoup(resp, "html5lib")
            classify_page = soup.find("div", class_="paginator").find_all("a")[-1]["href"]
            div_movies = soup.find("div", class_="grid-16-8 clearfix").find("div", class_="").find_all("table")
            for item in div_movies:
                detail_url = item.find_all("td")[0].find("a")["href"]
                queue_url.put([classify, detail_url, comment_count, "detail"])

            # print([classify, classify_page, comment_count, flag])
            queue_url.put([classify, classify_page, comment_count, flag])

        except error.HTTPError as ex:
            logging.error("Url_fetcher error: %s", ex)
    elif flag == "detail":
        get_detail(url)
    else:
        logging.error("Url: %s, Unknown flag :%s", url, flag)


def get_detail(detail_url):
    try:
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
        item_movie.better_than = re.sub(pattern="[\s]", repl="", string=(dou_beterthan.get_text().strip().replace("\n", ",")))

        for line in info.split("\n"):
            if line.find(":") > 0:
                list_info.append(line.strip())
        print(list_info)
        dict_info = {}
        for item in list_info:
            dict_info[item.split(":")[0]] = item.split(":")[1]
        for key in dict_info:
            print(key)
            print(dict_info[key])

        if len(list_info) == 10:
            item_movie.director, item_movie.screenwriter, item_movie.performer, item_movie.genre, \
            item_movie.country, item_movie.language, item_movie.release_time, item_movie.length, \
            item_movie.another_name, item_movie.imdb = list_info

        item_movie.url = url
        item_movie.img_url = mainpic.find("a").find("img").get("src")
        item_movie.name, item_movie.year = [item.get_text() for item in content.find("h1").find_all("span")]

        # print(item_movie.director, item_movie.screenwriter, item_movie.performer, item_movie.genre,
        #       item_movie.country, item_movie.language, item_movie.release_time, item_movie.length,
        #       item_movie.another_name, item_movie.imdb, item_movie.url, item_movie.img_url,
        #       item_movie.name, item_movie.year)
        # save_movies(item_movie)
    except error.HTTPError as ex:
        logging.error("Url_fetcher error: %s", ex)
    return


def save_movies(movie):
    engine = sqlalchemy.create_engine("mysql+pymysql://root:123@localhost:3306/db_doumovies?charset=utf8", echo=True)
    print("2222")
    db_session = sessionmaker(bind=engine)
    session = db_session()
    session.add(movie)
    session.commit()
    return


if __name__ == "__main__":
    # get_urls()
    # url_fetcher(queue_url.get())
    get_detail("https://movie.douban.com/subject/26340522/")
