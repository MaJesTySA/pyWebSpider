# -*- coding: utf-8 -*-
import scrapy

from DouBanBookList.items import BookItem


class BookSpiderSpider(scrapy.Spider):
    name = 'book_list_spider'
    allowed_domains = ['douban.com']
    start_urls = ['https://book.douban.com/series/33744',
                  'https://book.douban.com/series/23971']

    def parse(self, response):
        items = response.css('.subject-list .subject-item')
        next_page = response.css('.next a::attr(href)').extract_first()
        for item in items:
            book_item = BookItem()
            book_item['series'] = response.css('#wrapper #content h1::text').extract_first()
            book_item['cover'] = item.css('.pic img::attr(src)').extract_first()
            book_item['rating'] = item.css('.rating_nums::text').extract_first()
            book_item['count'] = item.css('.star.clearfix > span.pl::text').extract_first().replace('\n', '').replace(
                ' ', '')
            self.process_info(item, book_item)
            yield book_item
            if next_page != None:
                yield scrapy.Request(url=next_page, callback=self.parse)

    def process_info(self, item, book_item):
        #Process Infos
        infos = item.css('.pub::text').extract_first().replace('\n', '').replace(' ', '').split('/')
        book_item['author'] = infos[0]
        book_item['translator'] = infos[1]
        book_item['publish'] = infos[2]
        try:
            book_item['time'] = infos[3]
        except IndexError:
            book_item['time'] = None
        try:
            book_item['price'] = infos[4]
        except IndexError:
            book_item['price'] = None
        #Process Description
        description = item.css('.info p::text').extract_first()
        if description != None:
            book_item['description'] = description.replace('\n', '').replace(' ', '')
        #Process Title
        title = item.css('.info h2 a::text').extract_first()
        sub_title = item.css('.info h2 a span::text').extract_first()
        if sub_title != None:
            title = title + sub_title
        book_item['title'] = title.replace('\n','').replace(' ','')