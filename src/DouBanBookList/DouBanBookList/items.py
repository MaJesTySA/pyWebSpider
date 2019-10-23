import scrapy


class BookItem(scrapy.Item):
    cover = scrapy.Field()
    series = scrapy.Field()
    title = scrapy.Field()
    author = scrapy.Field()
    translator = scrapy.Field()
    publish = scrapy.Field()
    time = scrapy.Field()
    price = scrapy.Field()
    rating = scrapy.Field()
    count = scrapy.Field()
    description = scrapy.Field()
