# -*- coding: utf-8 -*-
import scrapy
import re
from selenium import webdriver
from selenium.webdriver import FirefoxOptions
from zhihu.items import AnswerItem,CommentItem,SecondCommentItem


class ZhihuSpiderSpider(scrapy.Spider):
    name = 'zhihu_spider'
    allowed_domains = ['www.zhihu.com']
    url_list = []

    def __init__(self):
        # 在初始化对象时，创建driver
        super(ZhihuSpiderSpider, self).__init__(name='zhihu_spider')
        option = FirefoxOptions()
        option.headless = True
        self.driver = webdriver.Firefox(options=option)

    def start_requests(self):
        base_url = self.settings.get("INIT_URL")
        for url in base_url:
            yield scrapy.Request(url, self.get_all_answer)

    def get_all_answer(self, response):
        ans_list = []
        answers = response.css('div[itemprop="zhihu:question"]')
        for answer in answers:
            ans_list.append("https://www.zhihu.com"+answer.css('a::attr(href)').extract_first())
        for single_url in ans_list:
            yield scrapy.Request(single_url, self.parse)

    def parse(self, response):
        answer_item = AnswerItem()
        answer_item['id'] = 0
        answer_item['question'] = response.css('h1[class="QuestionHeader-title"]::text').extract_first()
        answer_item['author'] = response.css('a[class="UserLink-link"]::text').extract_first()
        pattern = re.compile(r'<[^>]+>', re.S)
        answer_result = pattern.sub('', response.css('span[class="RichText ztext CopyrightRichText-richText"]').re_first('.*'))
        answer_item['answer'] = answer_result
        print(answer_item)
