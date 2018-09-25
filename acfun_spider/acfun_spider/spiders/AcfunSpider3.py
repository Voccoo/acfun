import scrapy
from acfun_spider.IpList import IPlist
import requests

# class Spider(scrapy.Spider):
#     name = 'ip'
#     allowed_domains = []
#
#     def start_requests(self):
#         url = 'http://www.baidu.com'
#         for ip in IPlist:
#             print(ip)
#             yield scrapy.Request(url=url, callback=self.parse, proxies={"http": ip}, dont_filter=True)
#
#     def parse(self, response):
#         print(response)
#测试ip地址是否可用
for ip in IPlist:

    try:
        r = requests.get('http://www.baidu.com', proxies={"http": ip}, timeout=8)
    except:
        print('connect failed' + ip)
    else:

        print('success' + ip)
