import requests
from scrapy.selector import Selector
import pymongo

client = pymongo.MongoClient('localhost')
db = client['proxy_ips']
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'}

def update_ips():
    response = requests.get('https://www.xicidaili.com/nn/', headers=headers)
    selector = Selector(text=response.text)
    pages = int(selector.css('.pagination a:nth-last-child(2)::text').extract_first())
    for i in range(1, pages):
        response = requests.get('https://www.xicidaili.com/nn/{0}'.format(i), headers=headers)
        selector = Selector(text=response.text)
        elements = selector.css('#ip_list tr')
        for element in elements[1:]:
            speed = element.css('.bar::attr(title)').extract_first()
            if speed:
                speed = float(speed.split('秒')[0])
            all_elements = element.css('td::text').extract()
            ip_addr = all_elements[0]
            port = all_elements[1]
            ip = {
                'ip_addr':ip_addr,
                'port':port,
                'speed':speed
            }
            db['proxy_ips'].insert_one(ip)

def get_random_ip():
    if db['proxy_ips'].find().count() == 0:
        update_ips()
        return get_random_ip()
    else:
        ips = db['proxy_ips'].find()
        for ip in ips:
            if check_ip_validation(ip):
                return 'http://{0}:{1}'.format(ip['ip_addr'], ip['port'])

def check_ip_validation(ip):
    url = 'http://www.baidu.com'
    proxy = 'http://{0}:{1}'.format(ip['ip_addr'],ip['port'])
    try:
        res = requests.get(url, proxies={'http':proxy},headers=headers)
    except requests.exceptions.ProxyError:
        print('invalid proxy ip')
        db['proxy_ips'].delete_one(ip)
        return False
    else:
        if res.status_code >=200 and res.status_code < 300:
            print('valid ip')
            return True
        else:
            print('invalid proxy ip')
            db['proxy_ips'].delete_one(ip)
            return False

if __name__ == '__main__':
    print(get_random_ip())
