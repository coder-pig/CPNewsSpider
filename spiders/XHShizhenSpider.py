"""
抓取新华时政的爬虫
"""
import datetime
import json
import re
import time
import requests as r

from tools.DBHelper import DBHelper, News

date_list = []
date_pattern = re.compile('(\d*?-\d*?-\d*? )', re.S)

headers = {
    'Host': 'www.xinhuanet.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.92 '
                  'Safari/537.36 ',
    'Referer': 'http://www.xinhuanet.com/politics/gd.htm'
}


def fetch_news():
    pg_num = 1
    news_list = []
    while True:
        resp = r.get("http://qc.wa.news.cn/nodeart/list?nid=113351&pgnum={}&cnt=35&tp=1&orderby=0&_={}"
                     .format(pg_num, int(round(time.time() * 1000))))
        if resp is not None:
            resp.encoding = 'utf-8'
            result_str = resp.text[1:-1]
            result_json = json.loads(result_str)
            for news in result_json['data']['list']:
                news_list.append(
                    News(news['Title'], news['Abstract'], news['LinkUrl'], news['PubTime'], '时政', "新华社"))
                if date_pattern.search(news['PubTime']).group(1)[:-1] not in date_list:
                    helper.insert_some_news(news_list)
                    return
            pg_num += 1


if __name__ == '__main__':
    helper = DBHelper()
    helper.create_db()
    helper.create_table()
    date_list = [str(datetime.date.today()), str(datetime.date.today() - datetime.timedelta(days=1))]
    fetch_news()
