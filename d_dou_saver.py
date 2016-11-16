# _*_ coding: utf-8 _*_

import time
import sqlalchemy
from queue import Queue
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from z_logcnf import log_init


def save_movies(queue_url, queue_save, logger):
    engine = sqlalchemy.create_engine("mysql+pymysql://root:123@localhost:3306/db_doumovies?charset=utf8", echo=True)
    # engine = sqlalchemy.create_engine("mysql+pymysql://root:mysql123@localhost:3306/db_doumovies?charset=utf8", echo=True)
    db_session = sessionmaker(bind=engine)
    session = db_session()
    while (queue_save.qsize() > 0) or (queue_url.qsize() > 0):
        if queue_save.qsize() == 0:
            logger.debug("saver want to run...%s", queue_save.qsize())
            time.sleep(150)
        else:
            logger.debug("saver is running...%s", queue_save.qsize())
            movie = queue_save.get()
            try:
                session.add(movie)
                session.commit()
                session.flush()
            except SQLAlchemyError as ex:
                session.rollback()
                logger.error("Saver error: %s, %s", movie.name, ex)
    return

if __name__ == '__main__':
    queue_url = Queue()
    queue_save = Queue()
    logger = log_init("saver")
    save_movies(queue_url, queue_save, logger)
