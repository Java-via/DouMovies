# _*_ coding: utf-8 _*_

import time
import sqlalchemy
from sqlalchemy.orm import sessionmaker


def save_movies(queue_url, queue_save):
    engine = sqlalchemy.create_engine("mysql+pymysql://root:123@localhost:3306/db_doumovies?charset=utf8", echo=True)
    db_session = sessionmaker(bind=engine)
    session = db_session()
    while (queue_save.qsize() > 0) or (queue_url.qsize() > 0):
        if queue_save.qsize() == 0:
            print("saver want to run...", queue_save.qsize())
            time.sleep(150)
        else:
            print("saver is running...", queue_save.qsize())
            movie = queue_save.get()
            print(movie)
            session.add(movie)
            session.commit()
            session.flush()
    return
