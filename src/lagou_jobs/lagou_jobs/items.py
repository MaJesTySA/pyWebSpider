# -*- coding: utf-8 -*-
import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, MapCompose, Join
from w3lib.html import remove_tags

from lagou_jobs.settings import SQL_DATETIME_FORMAT


def remove_splash(value):
    return value.replace('/','')

def handle_jobaddr(value):
    add_list = value.split('\n')
    add_list = [item.strip() for item in add_list if item.strip()!='查看地图']
    return ''.join(add_list)

class LagouItem(scrapy.Item):
    title = scrapy.Field()
    url = scrapy.Field()
    url_object_id = scrapy.Field()
    salary = scrapy.Field()
    job_city = scrapy.Field(
        input_processor = MapCompose(remove_splash)
    )
    work_years = scrapy.Field(
        input_processor = MapCompose(remove_splash)
    )
    degree_need = scrapy.Field(
        input_processor = MapCompose(remove_splash)
    )
    job_type = scrapy.Field()
    publish_time = scrapy.Field()
    tags = scrapy.Field(
        input_processor = Join(',')
    )
    job_advantage = scrapy.Field()
    job_desc = scrapy.Field()
    job_addr = scrapy.Field(
        input_processor=MapCompose(remove_tags, handle_jobaddr)
    )
    company_url = scrapy.Field()
    company_name = scrapy.Field()
    crawl_time = scrapy.Field()
    crawl_update_time = scrapy.Field()

    def get_insert_sql(self):
        insert_sql = """
            insert into lagou_job(title, url, url_object_id, salary, job_city, work_years, degree_need, 
            job_type, publish_time, job_advantage, job_desc, job_addr, company_name, company_url, 
            tags, crawl_time) 
            values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) 
            on duplicate key update salary=values(salary), job_desc=values(job_desc)
        """
        try:
            self.get('title')
        except:
            self['title']='None'

        params = (
            self['title'], self['url'], self['url_object_id'], self['salary'], self['job_city'],
            self['work_years'], self['degree_need'], self['job_type'], self['publish_time'],
            self['job_advantage'], self['job_desc'], self['job_addr'], self['company_name'],
            self['company_url'], self['tags'], self['crawl_time'].strftime(SQL_DATETIME_FORMAT)
        )
        return insert_sql,params

class LagouItemLoader(ItemLoader):
    default_output_processor = TakeFirst()