# _*_ coding: utf-8 _*_

import re
import time
import requests
from queue import Queue
from urllib import parse
from bs4 import BeautifulSoup
from pybloom import BloomFilter

from z_logcnf import log_init
from z_alche_movie import Movie


def url_parser(queue_fetch, queue_parse, queue_save, bf_url, logger):
    while (queue_fetch.qsize() > 0) or (queue_parse.qsize() > 0):
        logger.debug("parser is running...%s", queue_save.qsize())
        if queue_parse.qsize() == 0:
            time.sleep(3)
        else:
            classify, url_soup, comment_count, flag, repeat = queue_parse.get()
            logger.debug("parser is running...%s", queue_save.qsize())
            item_movie = Movie()
            # url = parse.quote(detail_url, safe="%/:=&?~#+!$,;'@()*[]|")
            if flag == "base":
                url, soup = url_soup
                try:
                    div_movies = soup.find("div", class_="grid-16-8 clearfix").find("div", class_="").find_all("table")
                    for item in div_movies:
                        detail_url = parse.urljoin(base="https://movie.douban.com/tag/",
                                                   url=item.find_all("td")[0].find("a")["href"])
                        logger.debug("Parse is running...%s get detail url...%s, %s, %s", queue_fetch.qsize(), detail_url, "detail", queue_parse.qsize())
                        if not bf_url.add(detail_url):
                            queue_fetch.put([classify, detail_url, comment_count, "detail", 2])

                    next_page = soup.find("div", class_="paginator").find_all("a")[-1].get_text()
                    if next_page.strip() == "后页>":
                        classify_next_page = soup.find("div", class_="paginator").find_all("a")[-1]["href"]
                        logger.debug("Parse is running...%s get base url...%s, %s, %s", queue_fetch.qsize(), classify_next_page, flag, queue_parse.qsize())
                        if not bf_url.add(classify_next_page):
                            queue_fetch.put([classify, classify_next_page, comment_count, flag, 3])
                    else:
                        logger.debug("This classify get all movies_url: %s", classify)
                except Exception as ex:
                    logger.error("Url_parser error: %s, Flag is %s, Url is %s", ex, flag, url)

            elif flag == "detail":
                url, soup = url_soup
                try:
                    soup = url_soup[1]
                    content = soup.find("div", id="content")
                    article = soup.find("div", class_="article")
                    mainpic = article.find("div", id="mainpic")

                    img_url = mainpic.find("a").find("img").get("src")
                    name, *year = [item.get_text() for item in content.find("h1").find_all("span")]

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

                    if not dict_info.get("集数"):
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
                        is_movie = 1
                    else:
                        director = dict_info.get("导演")
                        screenwriter = dict_info.get("编剧")
                        performer = dict_info.get("主演")

                        genre = dict_info.get("类型")
                        country = dict_info.get("制片国家/地区")
                        language = dict_info.get("语言")

                        release_time = dict_info.get("首播")
                        length = dict_info.get("单集片长") if dict_info.get("单集片长") else ""
                        length += "," + dict_info.get("集数") if dict_info.get("集数") else ""
                        another_name = dict_info.get("又名")
                        imdb = dict_info.get("IMDb链接")
                        is_movie = 0

                    item_movie.url = url_soup[0]
                    item_movie.img_url = img_url if img_url else ""
                    item_movie.name = name if name else ""
                    item_movie.year = year[0] if year else ""

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
                    item_movie.comment = comment if comment and ("目前" not in comment) else -1
                    item_movie.comment_this_classify = comment_count if comment_count else -1

                    item_movie.star_percent = star_percent if star_percent else ""
                    item_movie.better_than = better_than if better_than else ""
                    item_movie.imdb = imdb if imdb else ""
                    item_movie.is_movie = is_movie
                    item_movie.get_date = time.strftime("%Y-%m-%d")

                    # for test
                    # print(item_movie.url, item_movie.img_url, item_movie.name, item_movie.year,
                    #       item_movie.director, item_movie.screenwriter, item_movie.performer,
                    #       item_movie.genre, item_movie.country, item_movie.language,
                    #       item_movie.release_time, item_movie.length, item_movie.another_name,
                    #       item_movie.score, item_movie.comment, item_movie.comment_this_classify,
                    #       item_movie.star_percent, item_movie.better_than, item_movie.imdb, item_movie.is_movie)
                    queue_save.put(item_movie)
                    # for test
                    # save_movies(item_movie)
                except Exception as ex:
                    logger.error("Url_parser error: %s, flag is %s, Url is %s", ex, flag, url)
    return


if __name__ == '__main__':
    queue_fetch = Queue()
    queue_save = Queue()
    queue_parse = Queue()
    bf_url = BloomFilter(capacity=100000000, error_rate=0.01)
    dict_cookies = {"bid": "Thl_F4uF09U"}
    jar_cookies = requests.utils.cookiejar_from_dict(dict_cookies)
    req_session = requests.Session()
    req_session.cookies = jar_cookies
    logger = log_init("parser")
    url = "https://movie.douban.com/subject/2082328/"
    resp = req_session.get(url)
    soup = BeautifulSoup(resp.text, "html5lib")
    list_test = ["类型: 爱情", (url, soup), 1000, "detail", 3]
    queue_parse.put(list_test)
    print(queue_fetch.qsize())
    print(queue_parse.qsize())
    url_parser(queue_fetch, queue_parse, queue_save, bf_url, logger)
    print(queue_fetch.qsize())
    print(queue_parse.qsize())
