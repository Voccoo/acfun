# -*- coding: utf-8 -*-
import scrapy
import re
from acfun_spider.items import AcfunSpiderItem as acItem
import time
import random

from acfun_spider.settings import USER_AGENT as userAgent_list


class AcfunspiderSpider(scrapy.Spider):
    name = 'ac1'
    allowed_domains = ['acfun.cn']

    # 重写了start_request方法

    def start_requests(self):
        print('------爬取开始--------')
        for i in range(1506657, 13587900):  #266952 13587900
            url = "http://www.acfun.cn/u/%s.aspx" % str(i)
            if i == 13587900:
                print('------爬取完毕-------')
            user_agent = random.choice(userAgent_list)

            header = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                      'Accept-Encoding': 'gzip, deflate, br',
                      'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
                      'Connection': 'keep-alive',
                      'User-Agent': user_agent
                      }
            yield scrapy.Request(url=url, headers=header,  callback=self.parse)

    def parse(self, response):
        #print(response.status)
        try:
            item = acItem()
            nick_name = response.css('.name.fl.text-overflow::text').extract_first()
            sub = response.css('.fl.sub::text').extract_first()
            follow = response.css('.fl.follow::text').extract_first()
            fans = response.css('.fl.fans::text').extract_first()
            script_str = response.css('div[class="main"] script::text').extract_first()
            tan = response.css(".info.text-overflow.fl::text").extract_first()
            gender = re.findall(r'gender\":(.+?),\"signature', script_str)[0]
            uid = re.findall(r'userId\":(.+?),\"following', script_str)[0]

            # print(nick_name, '\n', sub, '\n', follow, '\n', fans, '\n', gender,'\n',tan)

            item['nick_name'] = nick_name
            item['sub'] = sub
            item['follow'] = follow
            item['fans'] = fans
            item['gender'] = gender
            item['tan'] = tan
            item['uid'] = uid

            yield item
        except:
            print('访问错误')
    pass

