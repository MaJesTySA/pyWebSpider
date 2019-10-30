# -*- coding: utf-8 -*-
import scrapy
import re

from CNBlogs_Articles.items import BlogItem


class CnblogsSpider(scrapy.Spider):
    name = 'cnblogs'
    allowed_domains = ['cnblogs.com']
    start_urls = ['https://www.cnblogs.com/']

    def parse(self, response):
        # 1. get every article url in the index page
        article_urls = response.css('#post_list .post_item .post_item_body h3 a::attr(href)').extract()
        for article_url in article_urls:
            # 2. parse one page
            yield scrapy.Request(url=article_url, callback=self.parse_one_page)
        # 3. get next index page
        next_url = response.xpath('// *[ @ id = "paging_block"] / div / a[last()]/@href').extract_first()
        if next_url:
            next_url = self.start_urls[0] + next_url
            yield scrapy.Request(url=next_url, callback=self.parse)

    def parse_one_page(self, response):

        item = BlogItem()


        item['title'] = response.xpath('//a[@class="postTitle2"]/text()').extract_first()
        item['time'] = response.xpath('//*[@id="post-date"]/text()').extract_first()
        item['url'] = response.url
        # Ajax request url needed
        author = re.findall('.*com/(.*?)/.*?', response.url)[0]
        blog_id = self.get_infos(response)[0]
        post_id = self.get_infos(response)[1]
        blog_user_guid = self.get_infos(response)[2]

        tags_url = 'https://www.cnblogs.com/{author}/ajax/CategoriesTags.aspx?blogId={blogId}&postId={postId}'
        view_url = 'https://www.cnblogs.com/{author}/ajax/GetViewCount.aspx?postId={postId}'
        info_url = 'https://www.cnblogs.com/{author}/ajax/BlogPostInfo.aspx?blogId={blogId}&postId={postId}&blogUserGuid={blogUserGuid}'

        yield scrapy.Request(url=tags_url.format(author=author, blogId=blog_id, postId=post_id),
                             callback=self.parse_tags, meta={'item': item})
        yield scrapy.Request(url=view_url.format(author=author, postId=post_id), callback=self.parse_view_count,
                             meta={'item': item})
        yield scrapy.Request(
            url=info_url.format(author=author, postId=post_id, blogId=blog_id, blogUserGuid=blog_user_guid),
            callback=self.parse_infos, meta={'item': item})

    def parse_article(self,response):
        pass

    def get_infos(self, response):
        html = response.text
        blog_id = re.findall('.*cb_blogId.*?(\d+).*', html)[0]
        post_id = re.findall('.*cb_entryId.*?(\d+).*cb.*', html)[0]
        blog_user_guid = re.findall(".*?cb_blogUserGuid.*?'(.*?)'.*", html)[0]
        return blog_id, post_id, blog_user_guid

    def parse_tags(self, response):
        item = response.meta['item']
        tags = response.xpath('//*[@id="EntryTag"]/a')
        if tags:
            item['tags'] = [tag.xpath('text()').extract_first() for tag in tags]
        yield item


    def parse_view_count(self, response):
        item = response.meta['item']
        item['view'] = str(response.body,'utf-8')
        yield item

    def parse_infos(self, response):
        item = response.meta['item']
        digg = response.xpath('//*[@id="digg_count"]/text()').extract_first()
        bury = response.xpath('//*[@id="bury_count"]/text()').extract_first()
        name = response.xpath('//*[@id="author_profile_detail"]/a[1]/text()').extract_first()
        item['digg'] = digg
        item['bury'] = bury
        item['name'] = name
        yield item
