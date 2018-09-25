# -*- coding: utf-8 -*-
import scrapy
from acfun_spider.items import AcfunSpiderItem as acItem
import random
import json
import pymysql

from acfun_spider.settings import USER_AGENT as userAgent_list

#scrapy爬虫，获取相关基础数据
class AcfunspiderSpider(scrapy.Spider):
    name = 'ac2'
    allowed_domains = ['acfun.cn']

    # 重写了start_request方法

    def start_requests(self):
        for i in range(1,13587900):  # 266952 13587900(1506657, 1506659)
            url = "http://www.acfun.cn/usercard.aspx?uid=%s" % str(i[0])
            user_agent = random.choice(userAgent_list)
            header = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                      'Accept-Encoding': 'gzip, deflate, br',
                      'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
                      'Connection': 'keep-alive',
                      'User-Agent': user_agent
                      }
            yield scrapy.Request(url=url, headers=header, callback=self.parse)




    def parse(self, response):
        # print(response.body)
        data = json.loads(response.body)
        if data['success']:
            try:
                item = acItem()
                nick_name = data['userjson'].get('name', '空').replace('\ue812', '')
                sub = data['userjson'].get('posts', '0')
                follow = data['userjson'].get('follows', '0')
                fans = data['userjson'].get('fans', '0')
                tan = data['userjson'].get('sign', '这个人很懒，什么都没有写...')
                gender = data['userjson'].get('gender', '0')
                uid = data['userjson'].get('uid', '0')
                comeFrom = data['userjson'].get('comeFrom', '未知')
                lastLoginTime = data['userjson'].get('lastLoginDate', '未知')
                regtime = data['userjson'].get('regTime', '未知')
                lastLoginIp = data['userjson'].get('lastLoginIp', '未知')

                item['nick_name'] = nick_name
                item['sub'] = sub
                item['follow'] = follow
                item['fans'] = fans
                item['gender'] = gender
                item['tan'] = tan
                item['uid'] = uid
                item['comeFrom'] = comeFrom
                item['lastLoginTime'] = lastLoginTime
                item['regtime'] = regtime
                item['lastLoginIp'] = lastLoginIp
                yield item
                # print(item)
            except:
                print('返回json错误')
        else:
            print('用户被封禁或者不存在')

    # 根据sql获取指定区间内的数据
    def get_all_data(self, sql):
        conn = pymysql.connect(host="localhost", user="root", passwd="Cs123456.", db="acfun", charset="utf8")
        cursor = conn.cursor()
        n = cursor.execute(sql)
        # print(type(n))
        data = cursor.fetchall()
        cursor.close()
        conn.close()

        return data
