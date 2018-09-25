# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class AcfunSpiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    nick_name = scrapy.Field()  # 昵称
    sub = scrapy.Field()  # 投稿数量
    follow = scrapy.Field()  # 关注数量
    fans = scrapy.Field()  # 粉丝数量
    gender = scrapy.Field()  # 性别 -1未知   0女    1男
    tan = scrapy.Field()  # 个性签名
    uid = scrapy.Field()  # user_id
    comeFrom = scrapy.Field()  # 来自
    lastLoginTime = scrapy.Field()  # 最后登录时间
    regtime = scrapy.Field()  # 注册时间
    lastLoginIp = scrapy.Field() #最后登录Ip
