import requests
from requests.exceptions import RequestException
import re
import csv


def get_one_page(url):
    try:
        response = requests.get(url, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.137 Safari/537.36 LBBROWSER'
        })
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        return None


def parse_one_page(html):
    pattern = re.compile('<dd>.*?board-index.*?>(\d+)</i>.*?name"><a'
                         + '.*?>(.*?)</a>.*?star">(.*?)</p>.*?releasetime">(.*?)</p>'
                         + '.*?integer">(.*?)</i>.*?fraction">(.*?)</i>.*?</dd>', re.S)
    items = re.findall(pattern, html)

    for item in items:
        yield [[
            item[0],
            item[1],
            item[4] + item[5],
            item[3].replace("上映时间：", ""),
            item[2].replace('\n', '').replace(' ', '').replace(",", "、").replace("主演：", "")]]


def write_to_file(content):
    with open('result.csv', 'a', encoding='utf-8-sig', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(content)


def main(offset):
    url = "https://maoyan.com/board/4?offset=" + str(offset)
    html = get_one_page(url)
    parse_one_page(html)
    for item in parse_one_page(html):
        write_to_file(item)


if __name__ == '__main__':
    rows = ['编号', '片名', '评分', '上映时间', '主演']
    with open('result.csv', 'a', encoding='utf-8-sig', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(rows)
    for i in range(10):
        main(10 * i)
