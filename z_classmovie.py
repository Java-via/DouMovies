# _*_ coding: utf-8 _*_


class Movie:
    def __init__(self, url, img_url, name, year, director, screenwriter,
                 performer, genre, country, language, release_time,
                 length, another_name, score, comment, star_percent, imdb):

        self.url = url
        self.img_url = img_url
        self.name = name
        self.year = year

        self.director = director
        self.screenwriter = screenwriter
        self.performer = performer

        self.genre = genre
        self.country = country
        self.language = language

        self.release_time = release_time
        self.length = length
        self.another_name = another_name

        self.score = score
        self.comment = comment
        self.star_percent = star_percent
        self.imdb = imdb
