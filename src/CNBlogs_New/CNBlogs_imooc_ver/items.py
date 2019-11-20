# -*- coding: utf-8 -*-
import re

import scrapy
from scrapy.loader.processors import MapCompose, TakeFirst, Identity, Join
from scrapy.loader import ItemLoader


def convert_date(value):
    match_date = re.match('.*?(\d+.*)', value)
    if match_date:
        return match_date.group(1)
    else:
        return '0000-00-00'


class BlogItem(scrapy.Item):
    title = scrapy.Field()
    content = scrapy.Field()
    url = scrapy.Field()
    url_object_id = scrapy.Field()
    front_image_path = scrapy.Field()
    digg_count = scrapy.Field()
    comments_count = scrapy.Field()
    view_count = scrapy.Field()
    tags = scrapy.Field(
        output_processor=Join(separator=',')
    )
    create_date = scrapy.Field(
        input_processor=MapCompose(convert_date)
    )
    front_image_url = scrapy.Field(
        output_processor=Identity()
    )


class BlogItemLoader(ItemLoader):
    default_output_processor = TakeFirst()
