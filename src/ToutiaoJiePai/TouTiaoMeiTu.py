import os
import re
from hashlib import md5
import requests
from urllib.parse import urlencode
from bs4 import BeautifulSoup
from requests.exceptions import RequestException
import json
from config import *
import pymongo
from multiprocessing import Pool

client = pymongo.MongoClient(MONGO_URL,connect=False)
db = client[MONGO_DB]

def get_page_index(offset, keyword):
    data = {
        'aid': 24,
        'app_name': 'web_search',
        'offset': offset,
        'format': 'json',
        'keyword': keyword,
        'autoload': 'true',
        'count': 20,
        'en_qc': 1,
        'cur_tab': 1,
        'from': 'search_tab',
        'pd': 'synthesis',
    }
    url = 'https://toutiao.com/api/search/content/?' + urlencode(data)

    try:
        response = requests.get(url, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.137 Safari/537.36 LBBROWSER',
        })
        response.encoding = 'utf-8'
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        print('请求异常')
        return None


def parse_page_index(html):
    data = json.loads(html)
    if data and 'data' in data.keys():
        for item in data.get('data'):
            yield item.get('article_url')


def get_page_detail(url):
    if url != None:
        try:
            response = requests.get(url, headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.137 Safari/537.36 LBBROWSER',
            })
            if response.status_code == 200:
                return response.text
            return None
        except RequestException:
            print('请求异常', url)
            return None
    return None


def parse_page_detail(html, url):
    soup = BeautifulSoup(html, 'lxml')
    title = soup.select('title')[0].get_text()
    images_pattern = re.compile('JSON.parse."(.*?)"\).*?sibling', re.S)
    result = re.search(images_pattern, html)
    if result:
        result = result.group(1).replace(r'\"', '"')
        data = json.loads(result)
        if data and 'sub_images' in data.keys():
            sub_images = data.get('sub_images')
            images = [item.get('url').replace('\\', '') for item in sub_images]
            for image in images:
                download_image(image)
            return {
                'title': title,
                'url': url,
                'images': images
            }


def save_to_mongo(result):
    if db[MONGO_TABLE].insert_one(result):
        print("存储成功")
        return True
    return False


def download_image(url):
    print('正在下载', url)
    try:
        response = requests.get(url)
        if response.status_code == 200:
            save_image(response.content)
        return None
    except RequestException:
        print("请求图片出错", url)
        return None


def save_image(content):
    file_path = '{0}/{1}.{2}'.format(os.getcwd()+'/imgs', md5(content).hexdigest(), 'jpg')
    if not os.path.exists(file_path):
        with open(file_path, 'wb') as f:
            f.write(content)
            f.close()


def main(offset):
    html = get_page_index(offset, KEYWORD)
    while json.loads(html)['count'] == 0:
        html = get_page_index(offset, KEYWORD)
    for url in parse_page_index(html):
        if url != None:
            html = get_page_detail(url)
            result = parse_page_detail(html, url)
            if result != None:
                save_to_mongo(result)


if __name__ == '__main__':
    groups=[x*20 for x in range(GROUP_START,GROUP_END+1)]
    pool=Pool()
    pool.map(main,groups)