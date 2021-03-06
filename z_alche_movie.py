# _*_ coding: utf-8 _*_

import sqlalchemy
from sqlalchemy.ext import declarative
# from sqlalchemy.orm import sessionmaker

engine = sqlalchemy.create_engine("mysql+pymysql://root:rootroot321@localhost:3306/db_doumovies?charset=utf8", echo=True)

BaseModel = declarative.declarative_base()


# 电影模型
class Movie(BaseModel):
    __tablename__ = "tb_doumovies"
    __table_args__ = {
        "mysql_engine": "InnoDB",
        "mysql_charset": "utf8"
    }

    id = sqlalchemy.Column(
        "m_id",
        sqlalchemy.INT,
        primary_key=True,
        autoincrement=True
    )
    url = sqlalchemy.Column(
        "m_url",
        sqlalchemy.VARCHAR(300)
    )
    img_url = sqlalchemy.Column(
        "m_imgurl",
        sqlalchemy.VARCHAR(300)
    )
    name = sqlalchemy.Column(
        "m_name",
        sqlalchemy.VARCHAR(300)
    )
    year = sqlalchemy.Column(
        "m_year",
        sqlalchemy.VARCHAR(50)
    )

    director = sqlalchemy.Column(
        "m_director",
        sqlalchemy.VARCHAR(500)
    )
    screenwriter = sqlalchemy.Column(
        "m_screenwriter",
        sqlalchemy.VARCHAR(500)
    )
    performer = sqlalchemy.Column(
        "m_performer",
        sqlalchemy.VARCHAR(1000)
    )

    genre = sqlalchemy.Column(
        "m_genre",
        sqlalchemy.VARCHAR(100)
    )
    country = sqlalchemy.Column(
        "m_country",
        sqlalchemy.VARCHAR(100)
    )
    language = sqlalchemy.Column(
        "m_language",
        sqlalchemy.VARCHAR(100)
    )

    release_time = sqlalchemy.Column(
        "m_releasetime",
        sqlalchemy.VARCHAR(100)
    )
    length = sqlalchemy.Column(
        "m_length",
        sqlalchemy.VARCHAR(500)
    )
    another_name = sqlalchemy.Column(
        "m_anothername",
        sqlalchemy.VARCHAR(500)
    )

    score = sqlalchemy.Column(
        "m_score",
        sqlalchemy.Float
    )
    comment = sqlalchemy.Column(
        "m_comment",
        sqlalchemy.INTEGER
    )
    comment_this_classify = sqlalchemy.Column(
        "m_all_comment",
        sqlalchemy.INTEGER
    )

    star_percent = sqlalchemy.Column(
        "m_starpercent",
        sqlalchemy.VARCHAR(500)
    )
    better_than = sqlalchemy.Column(
        "m_betterthan",
        sqlalchemy.VARCHAR(100)
    )
    imdb = sqlalchemy.Column(
        "m_imdb",
        sqlalchemy.VARCHAR(200)
    )
    is_movie = sqlalchemy.Column(
        "m_ismovie",
        sqlalchemy.SmallInteger
    )
    get_date = sqlalchemy.Column(
        "m_getdate",
        sqlalchemy.DATE
    )

# if __name__ == '__main__':
#     DBSession = sessionmaker(bind=engine)
#     session = DBSession()
#
#     session.add(Movie(url="www.baidu.com", img_url="www.baidu.com", name="模型", year="2016",
#                       director="导演", screenwriter="编辑", performer="演员",
#                       genre="类别", country="国家", language="语言",
#                       release_time="上映时间", length="时长", another_name="别名",
#                       score=10.0, comment="评价", star_percent="星级比例", imdb="imdb"))
#     session.commit()
