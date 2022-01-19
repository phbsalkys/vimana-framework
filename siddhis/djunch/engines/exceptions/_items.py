# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
#from scrapy.spiders import CrawlSpider, Rule
#from scrapy.linkextractors import LinkExtractor



class FuzzURLsPool(scrapy.Item):
    RAW_URLS = scrapy.Field() 
    UNICODE_URLS = scrapy.Field()       
    INT_TYPE_URLS = scrapy.Field()
    FLOAT_TYPE_URLS = scrapy.Field()
    OS_RANDOM_TYPE_URLS = scrapy.Field()
    SEC_RANDOM_TYPE_URLS = scrapy.Field()
    FULL_SCOPE = scrapy.Field()

class IssuesPool(scrapy.Item):
    ISSUES = scrapy.Field()

class ExceptionPool(scrapy.Item):
    ENTRIES = scrapy.Field()

class ConfigIssuesItem(scrapy.Item):
    IID = scrapy.Field()
    ISSUE_TYPE = scrapy.Field()
    URL = scrapy.Field()
    METHOD = scrapy.Field()
    COOKIE = scrapy.Field()
    RESPONSE = scrapy.Field()
    ISSUE = scrapy.Field()
    STATUS = scrapy.Field()

class ExceptionItem(scrapy.Item):
    IID = scrapy.Field()
    ISSUE_TYPE = scrapy.Field()
    EXCEPTION_COUNT = scrapy.Field()
    EXCEPTION_ID = scrapy.Field()
    EXCEPTION_TYPE = scrapy.Field() 
    EXCEPTION_ENV_VAR = scrapy.Field() 
    EXCEPTION_ENV_VALUE = scrapy.Field()
    EXCEPTION_REASON = scrapy.Field()
    EXCEPTION_TRACEBACK = scrapy.Field()
    ENVIRONMENT = scrapy.Field()
    EXCEPTION_SUMMARY = scrapy.Field()
    KEY_ENV_CONTEXTS = scrapy.Field()
    REQUEST_HEADERS = scrapy.Field()
    FUZZ_URLS_SCOPE = scrapy.Field()
    INSTALLED_ITEMS = scrapy.Field()
    DB_SETTINGS = scrapy.Field()
    CONTEXTS = scrapy.Field()
    OBJECTS = scrapy.Field()
    FINGERPRINT = scrapy.Field()



