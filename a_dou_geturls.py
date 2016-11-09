# _*_ coding: utf-8 _*_

import logging
from bs4 import BeautifulSoup
from urllib import request, parse, error


def get_urls(queue_url):
    list_url_tags = []
    print(queue_url.qsize())

    url = "https://movie.douban.com/tag/"
    try:
        cookie = "_vwo_uuid_v2=E3DF1C1851C8DCC6D914A081334D0A07|113f38aee5ecb34b708c3639c0c6d4b1;_" \
                 "pk_ref.100001.4cf6=%5B%22%22%2C%22%22%2C1478687617%2C%22https%3A%2F%2F" \
                 "www.baidu.com%2Fs%3Fwd%3D%25E8%25B1%2586%25E7%2593%25A3%26rsv_spt%3D1%26" \
                 "rsv_iqid%3D0x8cda56f40002035a%26issp%3D1%26f%3D8%26rsv_bp%3D0%26rsv_id" \
                 "x%3D2%26ie%3Dutf-8%26tn%3D99055797_hao_pg%26rsv_enter%3D1%26rsv_sug3%3D5%26" \
                 "rsv_sug1%3D5%26rsv_sug7%3D101%22%5D"
        headers = {"Accept-encoding": "utf-8",
                   "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) "
                                 "Chrome/41.0.2272.89 Safari/537.36",
                   "cookie": cookie}
        req = request.Request(url=url, data=None, headers=headers)
        resp = request.urlopen(req)
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
                queue_url.put([item_classify, url_classify, comment_count, "base"])
    except error.HTTPError as ex:
        logging.error("Get_urls error: %s", ex)
    print(queue_url.qsize())
    return queue_url

# if __name__ == '__main__':
#     get_urls(queue_url)
