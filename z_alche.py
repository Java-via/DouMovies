# _*_ coding: utf-8 _*_

import sqlalchemy
from sqlalchemy.ext import declarative

engine = sqlalchemy.create_engine("mysql+pymysql://root:123@localhost:3306/movie_db", encoding="utf8", echo=True)
connection = engine.connect()

connection = connection.execution_options(
    # 默认为 REPEATABLE READ connection.get_isolation_level()可查看
    isolation_level="READ COMMITTED"
)

BaseModel = declarative.declarative_base()

t = sqlalchemy.Table("dou_movie", metadata,)


# 电影模型
class Movie(BaseModel):
    __tablename__ = "dou_movie"
    __table_args__ = {
        "mysql_engine": "InnoDB",
        "mysql_charset": "utf8"
    }
