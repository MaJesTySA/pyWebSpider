import pymongo

import requests
from urllib.parse import urlencode
from requests.exceptions import ConnectionError
from pyquery import PyQuery as pq
from config import *

headers = {
    'Cookie': 'CXID=E102ADCAA3AD2AFC01C88873C5A3564B; SUID=9C0C73CA3765860A5D24554E0005BBD9; SUV=007C74F3CA730C9C5D2B0C1F78CD0130; ABTEST=0|1571211878|v1; IPLOC=CN5101; weixinIndexVisited=1; sct=1; SNUID=21FC823BF1F564F2B795390AF1D03A32; JSESSIONID=aaadt6Ds5cihfhPQW5r1w',
    'Host': 'weixin.sogou.com',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36'
}
# 全局proxy
proxy = None

client = pymongo.MongoClient('localhost')
db = client['WeChat']


def get_proxy():
    try:
        response = requests.get(PROXY_POOL_URL)
        if response.status_code == 200:
            return response.text
        return None
    except ConnectionError:
        return None


def get_html(url, count=1):
    print('Crawling', url)
    print('Trying Count', count)
    global proxy
    if count >= MAX_COUNT:
        print('Tried Too Many Counts')
        return None
    try:
        if proxy:
            proxies = {
                'http': 'http://' + proxy
            }
            response = requests.get(url, allow_redirects=False, headers=headers, proxies=proxies)
        else:
            response = requests.get(url, allow_redirects=False, headers=headers)
        if response.status_code == 200:
            return response.text
        if response.status_code == 302:
            proxy = get_proxy()
            if proxy:
                print('Using Proxy', proxy)
                return get_html(url)
            else:
                print('Get Proxy Failed')
                return None
    except ConnectionError as e:
        print('Error Occurred', e.args)
        proxy = get_proxy()
        count += 1
        return get_html(url, count)


def get_index(keyword, page):
    data = {
        'query': keyword,
        'type': 2,
        'page': page
    }
    queries = urlencode(data)
    url = BASE_URL + queries
    html = get_html(url)
    return html


def parse_index(html):
    doc = pq(html)
    items = doc('.news-box .news-list li .txt-box h3 a').items()
    for item in items:
        yield item.attr('data-share')


def get_detail(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        return None
    except ConnectionError:
        return None


def parse_detail(html):
    doc = pq(html)
    title = doc('.rich_media_title').text()
    content = doc('.rich_media_content').text()
    nickname = doc('.rich_media_meta_list .rich_media_meta_nickname a').text()
    return {
        'title': title,
        'content': content,
        'nickname': nickname
    }


def save_to_mongo(data):
    if db['articles'].update({'title': data['title']}, {'$set': data}, True):
        print('Saved to Mongo', data['title'])
    else:
        print('Saved to Mongo Failed', data['title'])


def main():
    for page in range(1, 101):
        html = get_index(KEYWORD, page)
        if html:
            article_urls = parse_index(html)
            for article_url in article_urls:
                article_html = get_detail(article_url)
                if article_html:
                    article_data = parse_detail(article_html)
                    save_to_mongo(article_data)


if __name__ == '__main__':
    main()
