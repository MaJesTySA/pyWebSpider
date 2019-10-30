# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BlogItem(scrapy.Item):
    title = scrapy.Field()
    tags = scrapy.Field()
    url = scrapy.Field()
    time = scrapy.Field()
    name = scrapy.Field()
    view = scrapy.Field()
    digg = scrapy.Field()
    bury = scrapy.Field()


