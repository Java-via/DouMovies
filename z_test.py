# _*_ coding: utf-8 _*_

import re
import redis
import logging
import pymysql
import functools
import operator

try:
    conn = pymysql.connect(host="54.169.79.230", user="appuser", passwd="123", db="db_doumovies", charset="utf8")
    r = redis.StrictRedis(host="54.169.79.230", port=6379, password="redis123", db="0", charset="utf-8")
    cur = conn.cursor()

    # cur.execute("select m_score, m_name from tb_doudou;")
    # score_name_all = [list(item) for item in cur.fetchall()]
    # print(score_name_all)
    # r.delete("all_movies")
    # r.zadd("all_movies", *functools.reduce(operator.add, score_name_all, []))
    # ss_all = r.zrange("all_movies", 0, 10, True, True)
    # print(list(map(lambda x: (x[0].decode(), x[1]), ss_all)))

    cur.execute("select m_score, m_name from tb_doudou WHERE CAST(m_comment AS signed)>1000 AND m_length!='';")
    score_name = [list(item) for item in cur.fetchall()]
    r.delete("movies")
    r.zadd("movies", *functools.reduce(operator.add, score_name, []))
    ss = r.zrange("movies", 0, 10, True, True)
    print(list(map(lambda x: (x[0].decode(), x[1]), ss)))

except Exception as ex:
    logging.error("select from mysql error: %s", ex)
