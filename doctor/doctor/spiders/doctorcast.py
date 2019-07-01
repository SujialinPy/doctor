# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from doctor.items import HospitalItem,DoctorItem,DepartmentItem
import re
from lxml import etree 
import ast

class DoctorcastSpider(scrapy.Spider):
	def __init__(self):
		super(DoctorcastSpider,self).__init__()
		self.remaining_links = len(self.start_urls)
	name = 'doctorcast'

	allowed_domains = ['haodf.com']
	start_urls = (
		'https://www.haodf.com/yiyuan/beijing/list.htm',
		'https://www.haodf.com/yiyuan/shanghai/list.htm',
		'https://www.haodf.com/yiyuan/guangdong/list.htm',
		'https://www.haodf.com/yiyuan/guangxi/list.htm',
		'https://www.haodf.com/yiyuan/jiangsu/list.htm',
		'https://www.haodf.com/yiyuan/zhejiang/list.htm',
		'https://www.haodf.com/yiyuan/anhui/list.htm',
		'https://www.haodf.com/yiyuan/jiangxi/list.htm',
		'https://www.haodf.com/yiyuan/fujian/list.htm',
		'https://www.haodf.com/yiyuan/shandong/list.htm',
		'https://www.haodf.com/yiyuan/sx/list.htm',
		'https://www.haodf.com/yiyuan/hebei/list.htm',
		'https://www.haodf.com/yiyuan/henan/list.htm',
		'https://www.haodf.com/yiyuan/tianjin/list.htm',
		'https://www.haodf.com/yiyuan/liaoning/list.htm',
		'https://www.haodf.com/yiyuan/heilongjiang/list.htm',
		'https://www.haodf.com/yiyuan/jilin/list.htm',
		'https://www.haodf.com/yiyuan/hubei/list.htm',
		'https://www.haodf.com/yiyuan/hunan/list.htm',
		'https://www.haodf.com/yiyuan/sichuan/list.htm',
		'https://www.haodf.com/yiyuan/chongqing/list.htm',
		'https://www.haodf.com/yiyuan/shanxi/list.htm',
		'https://www.haodf.com/yiyuan/gansu/list.htm',
		'https://www.haodf.com/yiyuan/yunnan/list.htm',
		'https://www.haodf.com/yiyuan/xinjiang/list.htm',
		'https://www.haodf.com/yiyuan/neimenggu/list.htm',
		'https://www.haodf.com/yiyuan/hainan/list.htm',
		'https://www.haodf.com/yiyuan/guizhou/list.htm',
		'https://www.haodf.com/yiyuan/qinghai/list.htm',
		'https://www.haodf.com/yiyuan/ningxia/list.htm',
		'https://www.haodf.com/yiyuan/xizang/list.htm',
		)
	rules = [
		Rule(LinkExtractor(allow=[r'/yiyuan/.+/\.list.htm']),callback='parse_yiyuan'),
		Rule(LinkExtractor(allow=[r'/hospital/.+\.htm']),callback='parse_hospital'),
		Rule(LinkExtractor(allow=[r'/faculty/.+\.htm']),callback='parse_faculty'),
		Rule(LinkExtractor(allow=[r'/doctor/.+\.htm']),callback='parse_doctor'),
	]
	
	def parse(self, response):
		self.remaining_links -= 1
		self.logger.info('parsing hospital list page -- %s ,剩余链接数：%d' % (response.url,self.remaining_links))
		hospital_links = response.xpath("//div[@class=\"m_ctt_green\"]/ul/li/a/@href") 	
		for link in hospital_links:
			self.remaining_links += 1
			yield scrapy.Request(response.urljoin(link.extract()),callback=self.parse_hospital,dont_filter=True,priority=900)

	def parse_hospital(self, response):
		self.remaining_links -= 1
		self.logger.info('parsing hospital page -- %s ,剩余链接数：%d'%(response.url,self.remaining_links))
		item = HospitalItem()
		item['link'] = response.url
		item['name'] = response.xpath('//h1[@class="hospital-name"]/text()').extract_first()
		self.logger.info('get Hospital item -- ' + item['name'])
		yield item
		faculty_links = response.xpath("//a[@class=\"f-l-i-s-i-w-name\"]/@href") 
		for link in faculty_links:
			self.remaining_links += 1
			yield scrapy.Request(response.urljoin(link.extract()),callback=self.parse_faculty,dont_filter=True,priority=800)

	def parse_faculty(self, response):
		self.remaining_links -= 1
		self.logger.info('parsing faculty page -- %s ,剩余链接数：%d'%(response.url,self.remaining_links))
		item = DepartmentItem()
		item['link'] = response.url
		item['name'] = response.xpath('//div[@class="content"]/a/text()').extract_first()
		self.logger.info('get faculty item -- ' + item['name'])
		yield item
		doctor_links = response.xpath("//a[@class=\"name\"]/@href") 
		for link in doctor_links:
			self.remaining_links += 1
			yield scrapy.Request(response.urljoin(link.extract()),callback=self.parse_doctor,dont_filter=True,priority=700)
		pnum_links = response.xpath("//a[@class=\"p_num\"]/@href")
		for link in pnum_links:
			self.remaining_links += 1
			yield scrapy.Request(response.urljoin(link.extract()),callback=self.parse_faculty,dont_filter=True,priority=800)
		
		
	def parse_doctor(self, response):
		self.remaining_links -= 1
		self.logger.info('parsing doctor page -- %s ,剩余链接数：%d'%(response.url,self.remaining_links))
		data = repr(ast.literal_eval(response.xpath('//script[1]')[1].extract()[55:-11])['content'].replace('\n','').replace('\t','')).replace(r'\\',"")[1:-1]
		html = etree.HTML(data)
		item = DoctorItem()
		item['link'] = response.url
		item['name'] = html.xpath("//div[@class='luj']/a[6]")[0].text
		item['hospital'] = html.xpath("//div[@class='luj']/a[4]")[0].text
		item['department'] = html.xpath("//div[@class='luj']/a[5]")[0].text
		yield item
		
