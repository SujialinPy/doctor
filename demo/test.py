# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymysql
class DoctorPipeline(object):
    def __init__(self):
        self.connect = pymysql.connect(
        host='127.0.0.1',#数据库地址
        port=3306,# 数据库端口
        db='doctor', # 数据库名
        user = 'root', # 数据库用户名
        passwd='liu998wei', # 数据库密码
        charset='utf8', # 编码方式
        use_unicode=True)

        # 通过cursor执行增删查改
        self.cursor = self.connect.cursor()

    def process_item(self, item):
        sql = "select name from dc_data where link='%s'" %(item['link'])
        self.cursor.execute(sql)
        result = self.cursor.fetchone()
        print(int(result[0]) > 2 or int(result[0]) + 1 > 2)
        if result:
            print("该链接已存在")
            return item
        else:
            print("执行插入操作")
            try:
                self.cursor.execute(
                    """insert into dc_data (link, name, hospital, department)
                    value (%s, %s, %s, %s)""",  # 纯属python操作mysql知识，不熟悉请恶补
                    (
                        item['link'], 
                        item['name'],
                        item['hospital'],
                        item['department']
                    )
                )
            except:
                self.cursor.execute(
                    """insert into dc_data (link, name)
                    value (%s, %s)""",  # 纯属python操作mysql知识，不熟悉请恶补
                    (
                        item['link'], 
                        item['name']
                    )
                )
            # 提交sql语句
            self.connect.commit()
            return item  # 必须实现返回
if __name__ == "__main__":
    item = {}
    item["link"] = "2"
    item["name"] = "2"
    item["hospital"] = 'hospital'
    item['department'] = "department1"
    pipe = DoctorPipeline()
    pipe.process_item(item)
