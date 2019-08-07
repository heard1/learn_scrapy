# -*- coding: utf-8 -*-
import scrapy
import re
import codecs
import json
from duoyinzi.items import DuoyinziItem

class DuoyinSpider(scrapy.Spider):
    name = 'duoyin'
    allowed_domains = ['zidian.911cha.com']
    start_urls = ['http://zidian.911cha.com/']

    def start_requests(self):
        url = []
        url1 = "https://zidian.911cha.com/duoyinzi.html"
        url.append(url1)
        next_url = "https://zidian.911cha.com/duoyinzi_{page}.html"
        for i in range(2,26):
            url.append(next_url.format(page=i))
        for i in url:
            yield scrapy.Request(i, self.get_all_word)


    def get_all_word(self, response):
        total = response.css('ul[class="l3 f16"] li')
        for one in total:
            wordurl = one.css('a::attr(href)').extract_first()
            yield scrapy.Request("https://zidian.911cha.com/"+wordurl, self.get_single_word)


    def get_single_word(self, response):
        word = response.css('span[class="f16 mr"]::text').extract_first()
        pron = []
        tem = response.css('div[class="mcon"]')
        tem = tem.xpath('./span/text()').extract()
        pattern = re.compile(u'[a-zà-ǜ]')
        tem = [x.strip() for x in tem]
        for i in tem:
            if pattern.match(i) and i not in pron:
                pron.append(i)
        res = {}
        res[word] = []
        for i in pron:
            tem={}
            tem[i]=[]
            res[word].append(tem)
        if len(response.css('div[class="mtb"]')) != 0:
            pat = re.compile(r'<[^>]+>', re.S)
            meaning = pat.sub('', response.css('.mtb').re('.*')[0])
            tem = re.findall("[1-9]、.*?。", meaning)
            k = -1
            for i in tem:
                if i[2]=='9' and i[3]=='1':
                    i = i[12:]
                if i[2]=='z' and i[3]=='i':
                    i = i[19:]
                if i[0] == '1':
                    k += 1
                res[word][k][pron[k]].append(i)

        lines = json.dumps(res, ensure_ascii=False)
        f = codecs.open('output/duoyinzi.json', 'a', 'utf-8')
        f.write(lines + '\n')
        f.close()

