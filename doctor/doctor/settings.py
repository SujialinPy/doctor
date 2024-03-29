# -*- coding: utf-8 -*-

# Scrapy settings for doctor project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html
from config.config import IF_USE_PROXY
import datetime
BOT_NAME = 'doctor'

SPIDER_MODULES = ['doctor.spiders']
NEWSPIDER_MODULE = 'doctor.spiders'

# LOG_LEVEL = 'DEBUG'
# to_day = datetime.datetime.now()
# log_file_path = 'doctor/logs/scrapy_{}_{}_{}.log'.format(to_day.year, to_day.month, to_day.day)
# LOG_FILE = log_file_path

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'doctor (+http://www.yourdomain.com)'
# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 10

# Configure a delay for requests for the same website (default: 0)
# See http://scrapy.readthedocs.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
CONCURRENT_REQUESTS_PER_DOMAIN = 10
# CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
# COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
DEFAULT_REQUEST_HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.8',
    'Accept-Encoding': 'gzip, deflate, br',
    'Content-Type': 'text/html;charset=UTF-8',
    'Cache-Control': 'no-cache',
}


# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'doctor.middlewares.DoctorSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
# DOWNLOADER_MIDDLEWARES = {
#    'doctor.middlewares.DoctorDownloaderMiddleware': 543,
# }

# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
   'doctor.pipelines.DoctorPipeline': 300,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See http://doc.scrapy.org/en/latest/topics/autothrottle.html
AUTOTHROTTLE_ENABLED = True
# The initial download delay
AUTOTHROTTLE_START_DELAY = 3
# The maximum download delay to be set in case of high latencies
AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'



# 默认使用 IP 代理池
if IF_USE_PROXY:
    DOWNLOADER_MIDDLEWARES = {

        # 第二行的填写规则
        #  yourproject.myMiddlewares(文件名).middleware类

        # 设置 User-Agent
        'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
        'proxyPool.scrapy.middlewares.RandomUserAgentMiddleware': 400,

        # 设置代理
        'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': None,
        'proxyPool.scrapy.middlewares.ProxyMiddleware': 100,

        # 设置自定义捕获异常中间层
        'proxyPool.scrapy.middlewares.CatchExceptionMiddleware': 105,

        # 设置自定义重连中间件
        'scrapy.downloadermiddlewares.retry.RetryMiddleware': None,
        'proxyPool.scrapy.middlewares.RetryMiddleware': 95,
    }
else:
    DOWNLOADER_MIDDLEWARES = {
        # 第二行的填写规则
        #  yourproject.myMiddlewares(文件名).middleware类
        'doctor.middlewares.DoctorDownloaderMiddleware': 543,

        # 设置 User-Agent
        'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
        'proxyPool.scrapy.middlewares.RandomUserAgentMiddleware': 400,
    }

