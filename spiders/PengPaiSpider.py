"""
抓取彭拜新闻的爬虫
"""
import re
import time

import requests as r

index_url = "https://www.thepaper.cn/"
ajax_url = "https://www.thepaper.cn/load_chosen.jsp?"
params_pattern = re.compile('(nodeids=\d.*?&topCids=.*?,&pageidx=)', re.S)
news_pattern = re.compile('<h2>.*?<a href="(.*?)" id.*?>(.*?)</a>.*?</p>.*?</h2>.*?<p>(.*?)</p>', re.S)  # 获取新闻信息的正则

headers = {
    'Referer': index_url,
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.92 '
                  'Safari/537.36 ',
}


def fetch_news():
    resp = r.get(index_url, headers=headers).text
    ajax_params = params_pattern.search(resp).group(1)
    time.sleep(1)
    headers["x-requested-with"] = "XMLHttpRequest"
    url = ajax_url + ajax_params + "1" + "&lastTime=" + str(int(round(time.time() * 1000)))
    ajax_resp = r.get(url, headers=headers).text
    print(ajax_resp)
    # results = news_pattern.findall(ajax_resp)
    # for result in results:
    #     print(result[0])
    #     print(result[1])
    #     print(result[2].replace("\n", "").strip())


if __name__ == '__main__':
    fetch_news()
