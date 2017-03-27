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
    name = "bhaskar"
    allowed_domains = ["bhaskar.com"]
    start_urls = (
        'http://www.bhaskar.com/',
    )

    def parse(self, response):
     
        news = Selector(response).xpath('//ul[@id="flicker_eknazar"]/li')
        print news
        for news in news:
            item = SamacharItem()
            item['title'] = news.xpath('p/a/text()').extract()[0]
            item['url'] = news.xpath('p/a/@href').extract()[0]
            item['img_title'] = news.xpath('div/a/@title').extract()[0]
            if news.xpath('div/a/img/@src').extract():
            	item['img_urls'] = news.xpath('div/a/img/@src').extract()[0]
            else:
                item['img_urls'] = news.xpath('div/a/img/@data-original').extract()[0]
            #item['shortdesc'] = news.xpath('p/text()').extract()[0]

            if item['url']:
                request = scrapy.Request(url=item['url'], callback=self.parse_detail_page, meta={'item':item}, dont_filter=True)   
            request.meta['item'] =item
            yield request

    def parse_detail_page(self, response):
        item = response.meta['item']
        detailPageSelector = Selector(response)
        item['description'] = detailPageSelector.xpath('//div[@id="fontSize-2" or @class="mainText"]/div').extract_first()
        
        yield item

