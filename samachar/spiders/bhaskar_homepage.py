# -*- coding: utf-8 -*-
import scrapy
import logging
import urlparse

from scrapy.spiders import Spider
from scrapy.selector import Selector
from samachar.items import SamacharItem
import re
import sys

class BhaskarSpider(scrapy.Spider):
    name = "bhaskar_homepage"
    allowed_domains = ["bhaskar.com"]
    start_urls = (
        'http://www.bhaskar.com/',
    )

    def parse(self, response):
     
        news = Selector(response).xpath('//div[@id="withoutajax"]/div/div[@class="eod-newsbox"]')
        
        for news in news:
            item = SamacharItem()
            item['title'] = news.xpath(
                'h5/a/text()').extract()[0]
            item['url'] = news.xpath(
                'h5/a/@href').extract()[0]
            item['img_urls'] = news.xpath('a/span/img/@src').extract()[0]
            item['shortdesc'] = news.xpath('p/text()').extract()[0]
            yield item

