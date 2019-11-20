# -*- coding: utf-8 -*-
from scrapy.pipelines.images import ImagesPipeline
import codecs
import json
from twisted.enterprise import adbapi


class BlogPipeline(object):
    def process_item(self, item, spider):
        return item

class FrontImagePipeline(ImagesPipeline):
    def item_completed(self, results, item, info):
        if 'front_image_url' in item:
            image_file_path = ''
            for ok, value in results:
                image_file_path = value['path']
            item['front_image_path'] = image_file_path
        return item


class AsyncMySQLPipeline(object):
    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):
        from MySQLdb.cursors import DictCursor
        dbparams = dict(
            host=settings['MYSQL_HOST'],
            db=settings['MYSQL_DBNAME'],
            user=settings['MYSQL_USER'],
            passwd=settings['MYSQL_PWD'],
            charset='utf8',
            cursorclass=DictCursor,
            use_unicode=True
        )
        dbpool = adbapi.ConnectionPool('MySQLdb', **dbparams)
        return cls(dbpool)

    def process_item(self, item, spider):
        query = self.dbpool.runInteraction(self.do_insert, item)
        query.addErrback(self.hand_error, item, spider)

    def do_insert(self, cursor, item):
        sql = 'insert into cnblogs_articles(title, url, url_object_id, front_image_url, front_image_path, digg_count, comments_count, view_count, tags, content, create_date)' \
              'values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) ON DUPLICATE KEY UPDATE content = VALUES(content)'
        params = list()
        params.append(item.get('title', ''))
        params.append(item.get('url', ''))
        params.append(item.get('url_object_id', ''))
        front_image = ','.join(item.get('front_image_url', []))
        params.append(front_image)
        params.append(item.get('front_image_path', ''))
        params.append(item.get('digg_count', 0))
        params.append(item.get('comments_count', 0))
        params.append(item.get('view_count', 0))
        params.append(item.get('tags', ''))
        params.append(item.get('content', ''))
        params.append(item.get('create_date', '1970-01-01'))
        cursor.execute(sql, tuple(params))

    def hand_error(self, failure, item, spider):
        print(failure)
