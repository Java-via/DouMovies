# _*_ coding: utf-8 _*_

import sqlalchemy
from sqlalchemy.orm import sessionmaker


def save_movies(queue_save):
    engine = sqlalchemy.create_engine("mysql+pymysql://root:123@localhost:3306/db_doumovies?charset=utf8", echo=True)
    db_session = sessionmaker(bind=engine)
    session = db_session()
    while queue_save.qsize() > 0:
        print(queue_save.qsize())
        movie = queue_save.get()
        session.add(movie)
        session.commit()
    return
