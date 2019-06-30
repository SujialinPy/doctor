# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class DoctorItem(scrapy.Item):
    # define the fields for your item here like:
    link = scrapy.Field()
    name = scrapy.Field()
    hospital = scrapy.Field()
    department = scrapy.Field()
class HospitalItem(scrapy.Item):
    link = scrapy.Field()
    name = scrapy.Field()

class DepartmentItem(scrapy.Item):
    link = scrapy.Field()
    name = scrapy.Field()


    
