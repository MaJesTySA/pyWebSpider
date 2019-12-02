# -*- coding: utf-8 -*-
import datetime
import time
import scrapy
import pickle
import base64
from mouse import move, click
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from zheye import zheye
from urllib import parse
import re
from scrapy.loader import ItemLoader
import json
from zhihuAnswer.items import ZhihuQuestionItem, ZhihuAnswerItem
import os


class ZhihuSpider(scrapy.Spider):
    name = 'zhihu'
    allowed_domains = ['www.zhihu.com']
    start_urls = ['http://www.zhihu.com/']
    start_answer_url = 'https://www.zhihu.com/api/v4/questions/{0}/answers?include=data%5B*%5D.is_normal%2Cadmin_closed_comment%2Creward_info%2Cis_collapsed%2Cannotation_action%2Cannotation_detail%2Ccollapse_reason%2Cis_sticky%2Ccollapsed_by%2Csuggest_edit%2Ccomment_count%2Ccan_comment%2Ccontent%2Ceditable_content%2Cvoteup_count%2Creshipment_settings%2Ccomment_permission%2Ccreated_time%2Cupdated_time%2Creview_info%2Crelevant_info%2Cquestion%2Cexcerpt%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%2Cis_labeled%2Cis_recognized%2Cpaid_info%2Cpaid_info_content%3Bdata%5B*%5D.mark_infos%5B*%5D.url%3Bdata%5B*%5D.author.follower_count%2Cbadge%5B*%5D.topics&offset={1}&limit={2}&sort_by=default&platform=desktop'

    def start_requests(self):
        cookie_dict = self.get_cookies()
        return [scrapy.Request(url=self.start_urls[0], dont_filter=True, cookies=cookie_dict)]

    def parse(self, response):
        all_urls = response.css('a::attr(href)').extract()
        all_urls = [parse.urljoin(response.url, url) for url in all_urls]
        all_urls = filter(lambda x: True if x.startswith('https') else False, all_urls)
        for url in all_urls:
            match_url = re.match('(.*zhihu.com/question/(\d+))(/|$).*', url)
            if match_url:
                request_url = match_url.group(1)
                question_id = match_url.group(2)
                yield scrapy.Request(request_url, callback=self.parse_question, meta={'question_id': question_id})
            else:
                yield scrapy.Request(url, callback=self.parse)

    #处理question页面，从中提取出QuestionItem。
    def parse_question(self, response):
        question_item_loader = ItemLoader(item=ZhihuQuestionItem(), response=response)
        question_item_loader.add_css('title', '.QuestionHeader-title::text')
        question_item_loader.add_css('content', '.QuestionHeader-detail')
        question_item_loader.add_value('url', response.url)
        question_item_loader.add_value('zhihu_id', int(response.meta.get('question_id')))
        question_item_loader.add_css('answer_num', '.List-headerText span::text')
        question_item_loader.add_css('comments_num', '.QuestionHeader-Comment button::text')
        question_item_loader.add_css('watch_user_num', '.NumberBoard-itemValue::text')
        question_item_loader.add_css('topics', '.QuestionHeader-topics .Popover div::text')
        question_item = question_item_loader.load_item()
        yield question_item
        yield scrapy.Request(self.start_answer_url.format(int(response.meta.get('question_id')), 0, 20), callback=self.parse_answer)

    # 发起ajax请求，得到AnswerItem。
    def parse_answer(self, response):
        ans_json = json.loads(response.text)
        is_end = ans_json['paging']['is_end']
        next_url = ans_json['paging']['next']
        for answer in ans_json['data']:
            answer_item = ZhihuAnswerItem()
            answer_item['zhihu_id'] = answer['id']
            answer_item['question_id'] = answer['question']['id']
            answer_item['url'] = answer['url']
            answer_item['author_id'] = answer['author']['id'] if 'id' in answer['author'] else None
            answer_item['content'] = answer['content'] if 'content' in answer else None
            answer_item['praise_num'] = answer['voteup_count']
            answer_item['comments_num'] = answer['comment_count']
            answer_item['create_time'] = answer['created_time']
            answer_item['update_time'] = answer['updated_time']
            answer_item['crawl_time'] = datetime.datetime.now()
            yield answer_item

        if not is_end:
            yield scrapy.Request(next_url, callback=self.parse_answer)

    def login(self):
        #启用chrome debug模式，防止识别chrome driver
        chrome_option = Options()
        chrome_option.add_argument('--disable-extensions')
        chrome_option.add_experimental_option('debuggerAddress', '127.0.0.1:9222')
        browser = webdriver.Chrome(chrome_options=chrome_option)

        #最大化窗口，保证屏幕坐标正确性
        try:
            browser.maximize_window()
        except:
            pass

        browser.get('https://www.zhihu.com/signin')
        browser.find_element_by_css_selector(
            "#root > div > main > div > div > div.Card.SignContainer-content > div > form > div.SignFlow-account > div > label > input").send_keys(
            Keys.CONTROL + "a")
        browser.find_element_by_css_selector(
            "#root > div > main > div > div > div.Card.SignContainer-content > div > form > div.SignFlow-account > div > label > input").send_keys(
            "your account")
        browser.find_element_by_css_selector(
            "#root > div > main > div > div > div.Card.SignContainer-content > div > form > div.SignFlow-tabs > div:nth-child(2)").click()
        browser.find_element_by_css_selector(
            "#root > div > main > div > div > div.Card.SignContainer-content > div > form > div.SignFlow-password > div > label > input").send_keys(
            Keys.CONTROL + "a")
        #故意输错密码，产生验证码
        browser.find_element_by_css_selector(
            "#root > div > main > div > div > div.Card.SignContainer-content > div > form > div.SignFlow-password > div > label > input").send_keys(
            "your pwd")
        browser.find_element_by_css_selector(
            "#root > div > main > div > div > div.Card.SignContainer-content > div > form > button").click()

        login_success = False

        if login_success:
            cookie_dict = self.update_cookies(browser)
            browser.close()
            return [scrapy.Request(url=self.start_urls[0], dont_filter=True, cookies=cookie_dict)]

        while not login_success:
            try:
                notify_ele = browser.find_element_by_css_selector(
                    '#root > div > div:nth-child(2) > header > div.AppHeader-inner > div.AppHeader-userInfo > div.Popover.PushNotifications.AppHeader-notifications')
                login_success = True
                cookie_dict = self.update_cookies(browser)
                browser.close()
                return [scrapy.Request(url=self.start_urls[0], dont_filter=True, cookies=cookie_dict)]
            except:
                pass

            try:
                eng_captcha_element = browser.find_element_by_class_name('Captcha-englishImg')
            except:
                eng_captcha_element = None

            try:
                chn_captcha_element = browser.find_element_by_class_name('Captcha-chineseImg')
            except:
                chn_captcha_element = None

            if chn_captcha_element:
                self.solve_chn_captcha(browser, chn_captcha_element)

            if eng_captcha_element:
                self.solve_eng_captcha(browser, eng_captcha_element)

    def solve_chn_captcha(self, browser, chn_captcha_element):
        location_x = chn_captcha_element.location['x']
        location_y = chn_captcha_element.location['y']
        # browser_panel_height = browser.execute_script('return window.outerHeight - window.innerHeight;')
        browser_panel_height = 70
        base64_img_text = chn_captcha_element.get_attribute('src')
        code = base64_img_text.replace('data:image/jpg;base64,', '').replace('%0A', '')
        img = open('zhihu_chn_captcha.jpeg', 'wb')
        img.write(base64.b64decode(code))
        img.close()
        z = zheye()
        positions = z.Recognize('zhihu_chn_captcha.jpeg')
        last_position = []
        if len(positions) == 2:
            if positions[0][1] > positions[1][1]:
                last_position.append([positions[1][1], positions[1][0]])
                last_position.append([positions[0][1], positions[0][0]])
            else:
                last_position.append([positions[0][1], positions[0][0]])
                last_position.append([positions[1][1], positions[1][0]])
            first_position = [int(last_position[0][0] / 2), int(last_position[0][1] / 2)]
            second_position = [int(last_position[1][0] / 2), int(last_position[1][1] / 2)]
            move(location_x + first_position[0], location_y + browser_panel_height + first_position[1])
            click()
            time.sleep(3)
            move(location_x + second_position[0], location_y + browser_panel_height + second_position[1])
            click()
        else:
            last_position.append([positions[0][1], positions[0][0]])
            first_position = [int(last_position[0][0] / 2), int(last_position[0][1] / 2)]
            move(location_x + first_position[0], location_y + browser_panel_height + first_position[1])
            click()
        self.input_account_and_login(browser)

    def solve_eng_captcha(self, browser, eng_captcha_element):
        base64_img_text = eng_captcha_element.get_attribute('src')
        code = base64_img_text.replace('data:image/jpg;base64,', '').replace('%0A', '')
        img = open('zhihu_eng_captcha.jpeg', 'wb')
        img.write(base64.b64decode(code))
        img.close()
        from zhihuAnswer.tools.ydm import YDMHttp
        ydm = YDMHttp('your_account', 'your_pwd', 9577, 'c7e973f213d6ea8e6411c455231e48fd')
        code = ydm.decode('zhihu_eng_captcha.jpeg', 5000, 60)
        while True:
            if code == '':
                code = ydm.decode('zhihu_eng_captcha.jpeg', 5000, 60)
            else:
                break
        time.sleep(5)
        browser.find_element_by_xpath(
            '//*[@id="root"]/div/main/div/div/div[1]/div/form/div[4]/div/div/label/input').send_keys(
            Keys.CONTROL + 'a')
        browser.find_element_by_xpath(
            '//*[@id="root"]/div/main/div/div/div[1]/div/form/div[4]/div/div/label/input').send_keys(code)
        self.input_account_and_login(browser)

    def input_account_and_login(self, browser):
        browser.find_element_by_css_selector(
            "#root > div > main > div > div > div.Card.SignContainer-content > div > form > div.SignFlow-account > div > label > input").send_keys(
            Keys.CONTROL + "a")
        browser.find_element_by_css_selector(
            "#root > div > main > div > div > div.Card.SignContainer-content > div > form > div.SignFlow-account > div > label > input").send_keys(
            "your_account")
        browser.find_element_by_css_selector(
            "#root > div > main > div > div > div.Card.SignContainer-content > div > form > div.SignFlow-password > div > label > input").send_keys(
            Keys.CONTROL + "a")
        browser.find_element_by_css_selector(
            "#root > div > main > div > div > div.Card.SignContainer-content > div > form > div.SignFlow-password > div > label > input").send_keys(
            "your_pwd")
        browser.find_element_by_css_selector(
            "#root > div > main > div > div > div.Card.SignContainer-content > div > form > button").click()

    def update_cookies(self, browser):
        cookies = browser.get_cookies()
        cookie_dict = {}
        for cookie in cookies:
            f = open('zhihuAnswer/cookies/zhihu/' + cookie['name'] + '.zhihu', 'wb')
            pickle.dump(cookie, f)
            f.close()
            cookie_dict[cookie['name']] = cookie['value']
        return cookie_dict

    def get_cookies(self):
        upper_dir = os.path.dirname(os.path.dirname(__file__))
        cookie_dir = os.path.join(upper_dir, 'cookies/zhihu')
        cookies_names = os.listdir(cookie_dir)
        cookie_dict = {}
        for cookie_name in cookies_names:
            with open(os.path.join(cookie_dir, cookie_name), 'rb') as f:
                cookie_file = pickle.load(f)
                cookie_dict[cookie_file['name']] = cookie_file['value']
        return cookie_dict
