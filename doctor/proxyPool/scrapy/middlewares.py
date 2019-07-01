# -*- coding: utf-8 -*-

import logging
import random
from proxyPool.ProxyPoolWorker import get_proxy_pool_worker

"""
请求处理工具
@Author monkey
@Date 2017-12-16
"""
class RandomUserAgentMiddleware(object): #400
    '''动态随机设置 User-agent'''
    UserAgent_List = [
        "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.1 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2226.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.4; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2225.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2225.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2224.3 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.93 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.93 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2049.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 4.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2049.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.67 Safari/537.36",
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.67 Safari/537.36",
        "Mozilla/5.0 (X11; OpenBSD i386) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1944.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.3319.102 Safari/537.36",
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.2309.372 Safari/537.36",
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.2117.157 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36",
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1866.237 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.137 Safari/4E423F",
        "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1",
        "Mozilla/5.0 (Windows NT 6.3; rv:36.0) Gecko/20100101 Firefox/36.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10; rv:33.0) Gecko/20100101 Firefox/33.0",
        "Mozilla/5.0 (X11; Linux i586; rv:31.0) Gecko/20100101 Firefox/31.0",
        "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:31.0) Gecko/20130401 Firefox/31.0",
        "Mozilla/5.0 (Windows NT 5.1; rv:31.0) Gecko/20100101 Firefox/31.0",
        "Opera/9.80 (X11; Linux i686; Ubuntu/14.10) Presto/2.12.388 Version/12.16",
        "Opera/9.80 (Windows NT 6.0) Presto/2.12.388 Version/12.14",
        "Mozilla/5.0 (Windows NT 6.0; rv:2.0) Gecko/20100101 Firefox/4.0 Opera 12.14",
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0) Opera 12.14",
        "Opera/9.80 (Windows NT 5.1; U; zh-sg) Presto/2.9.181 Version/12.00"
    ]
    def process_request(self, request, spider):
        logging.debug("======  RandomUserAgentMiddleware   process_request  ======")
        ua = random.choice(self.UserAgent_List)
        if ua:
            request.headers.setdefault('User-Agent', ua)
            request.headers.setdefault('Referer', request.url)
            # print(request.headers)

class ProxyMiddleware(object): #100
    '''代理IP中间件'''
    def process_request(self, request, spider):
        logging.debug("======  ProxyMiddleware   process_request  ======")
        # 设置代理IP
        proxy_address = get_proxy_pool_worker().select_proxy_data()
        logging.debug("=====  ProxyMiddleware get a random_proxy:【 {} 】 =====".format(proxy_address))
        request.meta['proxy'] = proxy_address

class CatchExceptionMiddleware(object): #105
    '''捕获异常中间层'''
    def process_exception(self, request, exception, spider):
        logging.debug("======  CatchExceptionMiddleware   process_exception  ======")
        try:
            proxy = request.meta['proxy']
            if 'http://' in proxy:
                proxy = proxy.replace('http://', '')
            else:
                proxy = proxy.replace('https://', '')

            get_proxy_pool_worker().plus_proxy_faild_time(proxy.split(':')[0])
        except Exception as e:
            logging.debug("===  访问页面: " + request.url + " 出现异常。\n %s", e)

    def process_responce(self, request, response, spider):
        logging.debug("======  CatchExceptionMiddleware   process_responce  ======")
        if response.staus < 200 or response.staus >= 400:
            try:
                proxy = request.meta['proxy']
                if 'http://' in proxy:
                    proxy = proxy.replace('http://', '')
                else:
                    proxy = proxy.replace('https://', '')

                get_proxy_pool_worker().plus_proxy_faild_time(proxy.split(':')[0])
            except KeyError:
                logging.debug("===  无法正常访问到的页面: " + response.url + " ===")
        return response

class RetryMiddleware(object): #95
    '''捕获重连中间层'''
    def process_exception(self, request, exception, spider):
        logging.debug("======  RetryMiddleware   process_exception  ======")
        try:
            proxy = request.meta['proxy']
            if 'http://' in proxy:
                proxy = proxy.replace('http://', '')
            else:
                proxy = proxy.replace('https://', '')

            get_proxy_pool_worker().plus_proxy_faild_time(proxy.split(':')[0])
            # print('ip  proxy  ===  ', proxy.split(':')[0])
        except Exception as e:
            logging.debug("===  访问页面: " + request.url + " 出现异常。\n %s", e)

    def process_responce(self, request, response, spider):
        logging.debug("======  RetryMiddleware   process_responce  ======")
        if response.staus < 200 or response.staus >= 400:
            try:
                proxy = request.meta['proxy']
                if 'http://' in proxy:
                    proxy = proxy.replace('http://', '')
                else:
                    proxy = proxy.replace('https://', '')

                get_proxy_pool_worker().plus_proxy_faild_time(proxy.split(':')[0])
            except KeyError:
                logging.debug("===  无法正常访问到的页面: " + response.url + " ===")
        return response
