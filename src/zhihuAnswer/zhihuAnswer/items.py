import datetime
import scrapy
from zhihuAnswer.settings import SQL_DATETIME_FORMAT
from zhihuAnswer.tools.common import extract_num


class ZhihuQuestionItem(scrapy.Item):
    zhihu_id = scrapy.Field()
    topics = scrapy.Field()
    url = scrapy.Field()
    title = scrapy.Field()
    content = scrapy.Field()
    answer_num = scrapy.Field(

    )
    comments_num = scrapy.Field()
    watch_user_num = scrapy.Field()
    click_num = scrapy.Field()
    crawl_time = scrapy.Field()

    def get_insert_sql(self):
        insert_sql = """
            insert into zhihu_question(zhihu_id, topics, url, title, content, answer_num, comments_num, watch_user_num, click_num, crawl_time) 
            values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            on duplicate key update content = values(content), answer_num = values(answer_num), comments_num = values(comments_num), watch_user_num = values(watch_user_num), 
            click_num = values(click_num)
        """
        zhihu_id = self['zhihu_id'][0]
        topics = ','.join(self['topics'])
        url = self['url'][0]
        title = self['title'][0]
        content = self['content'][0]
        try:
            self.get('answer_num')
            answer_num = extract_num(self['answer_num'][0])
        except:
            answer_num = 0
        try:
            self.get('comments_num')
            comments_num = extract_num(self['comments_num'][0])
        except:
            comments_num = 0

        if len(self['watch_user_num']) == 2:
            watch_user_num = int(self['watch_user_num'][0].replace(',', ''))
            click_num = int(self['watch_user_num'][1].replace(',', ''))
        else:
            watch_user_num = int(self['watch_user_num'][0].replace(',', ''))
            click_num = 0

        crawl_time = datetime.datetime.now().strftime(SQL_DATETIME_FORMAT)
        params = (
            zhihu_id, topics, url, title, content, answer_num, comments_num, watch_user_num, click_num, crawl_time)
        return insert_sql, params


class ZhihuAnswerItem(scrapy.Item):
    zhihu_id = scrapy.Field()
    question_id = scrapy.Field()
    url = scrapy.Field()
    author_id = scrapy.Field()
    content = scrapy.Field()
    praise_num = scrapy.Field()
    comments_num = scrapy.Field()
    create_time = scrapy.Field()
    update_time = scrapy.Field()
    crawl_time = scrapy.Field()

    def get_insert_sql(self):
        insert_sql = """
            insert into zhihu_answer(zhihu_id, url, question_id, author_id, content, praise_num, comments_num, create_time, update_time, crawl_time) 
            values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            on duplicate key update content = values(content), comments_num = values(comments_num), praise_num = values(praise_num), update_time = values(update_time)
        """
        create_time = datetime.datetime.fromtimestamp(self['create_time']).strftime(SQL_DATETIME_FORMAT)
        update_time = datetime.datetime.fromtimestamp(self['update_time']).strftime(SQL_DATETIME_FORMAT)
        params = (self['zhihu_id'], self['url'], self['question_id'], self['author_id'], self['content'],
                  self['praise_num'], self['comments_num'], create_time, update_time,
                  self['crawl_time'])
        return insert_sql, params
