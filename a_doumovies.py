# _*_ coding: utf-8 _*_

import logging
from queue import Queue
from bs4 import BeautifulSoup
from urllib import request, parse, error
from z_classmovie import *

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
                url_classify = parse.urljoin(base="https://movie.douban.com/tag/%E7%88%B1%E6%83%85", url=item.a["href"])
                classify_comment = item.get_text().replace(")", "").split("(")
                item_classify = list_title[i] + ":" + classify_comment[0]
                comment_count = classify_comment[1]
                list_url_tags.append([item_classify, url_classify, comment_count, "base"])
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
        try:
            item_movie = Movie
            url = parse.quote("https://movie.douban.com/subject/26280528/", safe="%/:=&?~#+!$,;'@()*[]|")
            header = {"Accept-encoding": "utf-8"}
            req = request.Request(url=url, headers=header)
            resp = request.urlopen(req)
            soup = BeautifulSoup(resp, "html5lib")

        except error.HTTPError as ex:
            logging.error("Url_fetcher error: %s", ex)


def get_detail():
    try:
        item_movie = Movie
        url = parse.quote("https://movie.douban.com/subject/26280528/", safe="%/:=&?~#+!$,;'@()*[]|")
        header = {"Accept-encoding": "utf-8"}
        req = request.Request(url=url, headers=header)
        resp = request.urlopen(req)
        soup = BeautifulSoup(resp, "html5lib")
        content = soup.find("div", id="content")
        article = soup.find("div", class_="article")
        mainpic = article.find("div", id="mainpic")
        info = article.find("div", id="info").get_text()
        list_info = []

        for line in info.split("\n"):
            if line.find(":") > 0:
                list_info.append(line.strip().split(":")[1])

        if len(list_info) == 10:
            item_movie.director, item_movie.screenwriter, item_movie.performer, item_movie.genre, \
            item_movie.country, item_movie.language, item_movie.release_time, item_movie.length, \
            item_movie.another_name, item_movie.imdb = list_info

        item_movie.url = url
        item_movie.img_url = mainpic.find("a").find("img").get("src")
        item_movie.name, item_movie.year = [item.get_text() for item in content.find("h1").find_all("span")]

        print(item_movie.director, item_movie.screenwriter, item_movie.performer, item_movie.genre,
              item_movie.country, item_movie.language, item_movie.release_time, item_movie.length,
              item_movie.another_name, item_movie.imdb, item_movie.url, item_movie.img_url, item_movie.name, item_movie.year)

    except error.HTTPError as ex:
        logging.error("Url_fetcher error: %s", ex)


if __name__ == "__main__":
    # get_urls()
    # url_fetcher(queue_url.get())
    get_detail()
