# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql


class AcfunSpiderPipeline(object):
    comments = []

    def open_spider(self, spider):
        self.conn = pymysql.connect(host="localhost", user="root", passwd="Cs123456.", db="acfun", charset="utf8")
        self.cursor = self.conn.cursor()

    def insert_to_sql(self, data):
        try:
            sql = "insert into user_info (nick_name,sub,follow,fans,gender,tan,uid,regtime,lastLoginTime,comeFrom,lastLoginIp) values(%s, %s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            # print(data)
            self.cursor.executemany(sql, data)
            self.conn.commit()
        except:
            print('数据插入有误。。')
            self.conn.rollback()

    def process_item(self, item, spider):

        self.comments.append(
            [item['nick_name'], item['sub'], item['follow'], item['fans'], item['gender'], item['tan'], item['uid'],
             item['regtime'], item['lastLoginTime'], item['comeFrom'], item['lastLoginIp']])
        if len(self.comments) == 100:
            self.insert_to_sql(self.comments)
            # 清空缓冲区
            self.comments.clear()
        return item

    def close_spider(self, spider):
        # print( "closing spider,last commit", len(self.comments))
        self.insert_to_sql(self.comments)
        self.conn.commit()
        self.cursor.close()
        self.conn.close()
