# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from urllib import parse
import json
import re

from CNBlogs_imooc_ver.items import BlogItem, BlogItemLoader
from CNBlogs_imooc_ver.utils import common


class CnblogsSpider(scrapy.Spider):
    name = 'cnblogs'
    allowed_domains = ['news.cnblogs.com']
    start_urls = ['http://news.cnblogs.com/']

    def parse(self, response):
        post_nodes = response.css('#news_list .news_block')
        for post_node in post_nodes:
            image_url = post_node.css('.entry_summary a img::attr(src)').extract_first()
            #解决部分以//开头的图片url
            if image_url!=None and image_url.startswith('//'):
                image_url = 'https:' + image_url
            post_url = post_node.css('h2 a::attr(href)').extract_first()
            yield Request(url=parse.urljoin(response.url, post_url), meta={'front_image_url': image_url},
                          callback=self.parse_detail)
        #爬取下一页
        next_url = response.xpath("//a[contains(text(), 'Next >')]/@href").extract_first()
        yield Request(url=parse.urljoin(response.url, next_url), callback=self.parse)

    def parse_detail(self, response):
        post_id = re.match('.*?(\d+)', response.url)
        if post_id:
            post_id = post_id.group(1)
            item_loader = BlogItemLoader(item=BlogItem(), response=response)
            item_loader.add_css('title', '#news_title a::text')
            item_loader.add_css('content', '#news_content')
            item_loader.add_css('tags', '.news_tags a::text')
            item_loader.add_css('create_date', '#news_info .time::text')
            item_loader.add_value('url', response.url)
            if response.meta.get('front_image_url', []):
                item_loader.add_value('front_image_url', response.meta.get('front_image_url', []))
            yield Request(url=parse.urljoin(response.url, '/NewsAjax/GetAjaxNewsInfo?contentId={}'.format(post_id)),
                          meta={'item_loader': item_loader, 'url': response.url}, callback=self.parse_info)

    def parse_info(self, response):
        json_data = json.loads(response.text)
        item_loader = response.meta.get('item_loader', '')
        item_loader.add_value('digg_count', json_data['DiggCount'])
        item_loader.add_value('view_count', json_data['TotalView'])
        item_loader.add_value('comments_count', json_data['CommentCount'])
        item_loader.add_value('url_object_id', common.get_md5(response.meta.get('url', '')))
        yield item_loader.load_item()
