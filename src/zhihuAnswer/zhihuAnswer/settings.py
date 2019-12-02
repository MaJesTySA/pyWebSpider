# -*- coding: utf-8 -*-
BOT_NAME = 'zhihuAnswer'

SPIDER_MODULES = ['zhihuAnswer.spiders']
NEWSPIDER_MODULE = 'zhihuAnswer.spiders'

ROBOTSTXT_OBEY = False

COOKIES_ENABLED = True
COOKIES_DEBUG = True
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36"

MYSQL_HOST = '127.0.0.1'
MYSQL_DBNAME = 'zhihu_answers'
MYSQL_USER = 'root'
MYSQL_PWD = ''
SQL_DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'
SQL_DATE_FORMAT = '%Y-%m-%d'

DOWNLOADER_MIDDLEWARES = {
   'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': 2,
}

ITEM_PIPELINES = {
   'zhihuAnswer.pipelines.AsyncMySQLPipeline': 300,
}

