# -*- coding: utf-8 -*-
import os

BOT_NAME = 'CNBlogs_imooc_ver'

SPIDER_MODULES = ['CNBlogs_imooc_ver.spiders']
NEWSPIDER_MODULE = 'CNBlogs_imooc_ver.spiders'

ROBOTSTXT_OBEY = False

IMAGES_STORE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'images')
IMAGES_URLS_FIELD = 'front_image_url'

MYSQL_HOST = '127.0.0.1'
MYSQL_DBNAME = 'cnblogs_spider'
MYSQL_USER = 'root'
MYSQL_PWD = 'z55182182'

ITEM_PIPELINES = {
    'CNBlogs_imooc_ver.pipelines.BlogPipeline': 300,
    'CNBlogs_imooc_ver.pipelines.FrontImagePipeline': 1,
    'CNBlogs_imooc_ver.pipelines.AsyncMySQLPipeline':2
}
