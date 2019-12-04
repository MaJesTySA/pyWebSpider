# -*- coding: utf-8 -*-
import datetime
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from lagou_jobs.items import LagouItemLoader, LagouItem
from lagou_jobs.utils.common import get_md5
import os
import pickle
from selenium import webdriver
import time

class LagouSpider(CrawlSpider):
    name = 'lagou'
    allowed_domains = ['www.lagou.com']
    start_urls = ['https://www.lagou.com/']

    rules = (
        Rule(LinkExtractor(allow=('zhaopin/.*',)), follow=True),
        Rule(LinkExtractor(allow=('gongsi/j\d+.html',)), follow=True),
        Rule(LinkExtractor(allow=r'jobs/\d+.html'), follow=True, callback='parse_job'),
    )

    def start_requests(self):
        cookies = []
        if os.path.exists('lagou_jobs/cookies/lagou.cookies'):
            cookies = pickle.load(open('lagou_jobs/cookies/lagou.cookies', 'rb'))
        else:
            self.update_cookies()
        cookies_dict = {}
        for cookie in cookies:
            cookies_dict[cookie['name']] = cookie['value']
        for url in self.start_urls:
            yield scrapy.Request(url, dont_filter=True, cookies=cookies_dict)

    def parse_job(self, response):
        if response.url.find('utrack') > -1:
            self.update_cookies()
        else:
            item_loader = LagouItemLoader(item=LagouItem(), response=response)
            item_loader.add_css('title','.job-name::attr(title)')
            item_loader.add_value('url', response.url)
            item_loader.add_value('url_object_id', get_md5(response.url))
            item_loader.add_css('salary', '.job_request .salary::text')
            item_loader.add_xpath('job_city', "//*[@class='job_request']/h3/span[2]/text()")
            item_loader.add_xpath('work_years', "//*[@class='job_request']/h3/span[3]/text()")
            item_loader.add_xpath('degree_need', "//*[@class='job_request']/h3/span[4]/text()")
            item_loader.add_xpath('job_type', "//*[@class='job_request']/h3/span[5]/text()")
            item_loader.add_css('tags', '.position-label li::text')
            item_loader.add_css('publish_time', '.publish_time::text')
            item_loader.add_css('job_advantage', '.job-advantage p::text')
            item_loader.add_css('job_desc', '.job_detail')
            item_loader.add_css('job_addr', '.work_addr')
            item_loader.add_css('company_name', '#job_company dt a img::attr(alt)')
            item_loader.add_css('company_url', '#job_company dt a::attr(href)')
            item_loader.add_value('crawl_time', datetime.datetime.now())

            job_item = item_loader.load_item()
            return job_item

    def update_cookies(self):
        browser = webdriver.Chrome()
        browser.get('https://passport.lagou.com/login/login.html')
        browser.find_element_by_css_selector(
            'body > section > div.left_area.fl > div.form-content > div:nth-child(2) > form > div:nth-child(1) > input').send_keys(
            'your account')
        browser.find_element_by_css_selector('.form_body input[type="password"]').send_keys('your pwd')
        browser.find_element_by_css_selector(
            'body > section > div.left_area.fl > div.form-content > div:nth-child(2) > form > div.input_item.btn_group.clearfix.sense_login_password > input').click()
        time.sleep(5)
        cookies = browser.get_cookies()
        pickle.dump(cookies, open('lagou_jobs/cookies/lagou.cookies', 'wb'))