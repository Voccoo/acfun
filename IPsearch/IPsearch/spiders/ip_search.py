# -*- coding: utf-8 -*-
import scrapy
import random
from IPsearch.userAgent import USER_AGENT_LIST as userAgent_list
import pymysql


class IpSearchSpider(scrapy.Spider):
    name = 'ip_s'
    allowed_domains = ['ip.cn']

    # start_urls = ['http://baidu.com/']

    def start_requests(self):
        conn = pymysql.connect(host="localhost", user="root", passwd="Cs123456.", db="acfun", charset="utf8")
        cursor = conn.cursor()
        #sql = "select lastLoginIp,count(*) from user_info where lastLoginIp is not null and (comeFrom = '未知' or comeFrom is NULL or comeFrom='') group by lastLoginIp HAVING count(*) >=1"
        sql = "select lastLoginIp ,count(*) from user_info where (comeFrom is  null or comeFrom ='' or comeFrom='未知') and lastLoginIp is not null and lastLoginTime >= '2018-01-01 00:00:00'GROUP BY lastLoginIp HAVING count(*)>=1"
        cursor.execute(sql)
        datas = cursor.fetchall()
        cursor.close()
        conn.close()
        for data in datas:
            # data[0][:-1],'0'
            ip = data[0][:-1] + '0'

            user_agent = random.choice(userAgent_list)
            headers = {
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,* /*;q = 0.8',
                'accept - encoding': 'gzip,deflate,br',
                'accept - language': ' zh - CN, zh;q = 0.9',
                'upgrade-insecure-requests': '1',
                'user-agent': user_agent
            }
            url = 'https://ip.cn/index.php?ip=%s' % ip

            yield scrapy.Request(url=url, headers=headers, callback=self.parse)
        # ip='112.5.234.0'
        # user_agent = random.choice(userAgent_list)
        # headers = {
        #     'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,* /*;q = 0.8',
        #     'accept - encoding': 'gzip,deflate,br',
        #     'accept - language': ' zh - CN, zh;q = 0.9',
        #     'upgrade-insecure-requests': '1',
        #     'user-agent': user_agent
        # }
        # url = 'https://ip.cn/index.php?ip=%s' % ip
        #
        # yield scrapy.Request(url=url, headers=headers, callback=self.parse)

    def parse(self, response):
        ip = response.url[27:-1] + '*'
        # data = response.css('.well p:nth-child(2) code:text').extract_first()
        data = response.xpath('//*[@id="result"]/div/p[2]/code/text()').extract_first()
        address = data.split(' ')[0]

        sql = "when '%s' then '%s'" % (ip, address)

        with open('I:/Acfun/IPsearch/resutl/sql_ip_9-25.txt', 'a+') as f:
            f.write(sql + '\n')
            f.close()
