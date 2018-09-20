"""
抓取新华社新闻的爬虫
"""
import requests as r
from bs4 import BeautifulSoup
import re
import datetime
import time
import json

from tools.DBHelper import DBHelper, News

this_moment = ''  # 当前时间
xhjj_url = 'http://www.news.cn/xhjj.htm'  # 新华聚焦
politics_url = 'http://www.xinhuanet.com/politics/'  # 新华时政
qqbb_url = 'http://www.xinhuanet.com/world/qqbb.htm'  # 全球播报
normal_jquery_base_url = 'http://qc.wa.news.cn/nodeart/list'  # 普通加载更多新闻的基地址
date_verify = re.compile(r'<span( class="time")?>(.*?)</span>', re.S)  # 提取日期的正则
default_headers = {
    'Host': 'www.xinhuanet.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.92 '
                  'Safari/537.36 '
}


# 提取新华聚焦的新闻
def fetch_xhjj():
    resp = r.get(xhjj_url, headers=default_headers)
    resp.encoding = 'utf8'
    bs = BeautifulSoup(resp.text, 'lxml')
    li_s = bs.select('ul.dataList > li.clearfix')
    news_list = []
    for li in li_s:
        news_list.append(News(li.h3.text, li.h3.a.attrs.get('href'), date_verify.search(str(li)).group(2), "新华社"))
    helper.insert_some_news(news_list)


# 提取时政信息
def fetch_politics():
    params = {'nid': '113352', 'cnt': '10', 'tp': '1'}
    page_count = 1
    news_time = ''  # 新闻的时间
    news_list = []
    while True:
        params['pgnum'] = page_count
        params['_'] = str(int(time.time()))
        resp = r.get(normal_jquery_base_url, params=params, headers=default_headers).text[1:-1]
        result_json = json.loads(resp)
        for news in result_json['data']['list']:
            news_list.append(News(news['Title'], news['LinkUrl'], news['PubTime'], "新华社"))
            news_time = news['PubTime']
        page_count += 1
        if get_date_differ(this_moment, news_time) > 2:
            break
    helper.insert_some_news(news_list)


# 获得全球播报
def fetch_qqbb():
    resp = r.get(qqbb_url, headers=default_headers)
    resp.encoding = 'utf-8'
    bs = BeautifulSoup(resp.text, 'lxml')
    li_s = bs.select('ul.dataList > li.clearfix')
    news_list = []
    for li in li_s:
        news_list.append(News(li.h3.text, li.h3.a.attrs.get('href'), date_verify.search(str(li)).group(2), "新华社"))
    helper.insert_some_news(news_list)


# 获取财经信息
def fetch_fortune():
    params = {'nid': '11147664', 'cnt': '10', 'tp': '1'}
    page_count = 1
    news_time = ''  # 新闻的时间
    while True:
        params['pgnum'] = page_count
        params['_'] = str(int(time.time()))
        resp = r.get(normal_jquery_base_url, params=params, headers=default_headers).text[1:-1]
        result_json = json.loads(resp)
        news_list = []
        for news in result_json['data']['list']:
            news_list.append(News(news['Title'], news['LinkUrl'], news['PubTime'], "新华社"))
            news_time = news['PubTime']
        page_count += 1
        if get_date_differ(this_moment, news_time) > 1:
            break
    helper.insert_some_news(news_list)


# 返回两个时间字符串的天数差
def get_date_differ(date_1, date_2):
    d1 = datetime.datetime.strptime(date_1, '%Y-%m-%d %H:%M:%S')
    d2 = datetime.datetime.strptime(date_2, '%Y-%m-%d %H:%M:%S')
    return (d1 - d2).days


if __name__ == '__main__':
    this_moment = time.strftime('%Y-%m-%d %H:%M:%S')
    helper = DBHelper()
    helper.create_db()
    helper.create_table()
    fetch_xhjj()
    fetch_politics()
    fetch_qqbb()
    fetch_fortune()
