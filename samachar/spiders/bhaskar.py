# -*- coding: utf-8 -*-
import scrapy
import logging
import urllib.parse

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
     
        newss = Selector(response).xpath('//div[@class="swiper-wrapper trendNav orangeNav"]')
        #print news
        for news in newss:
            item = SamacharItem()
            item['title'] = news.xpath('div/a/text()').extract_first()
            item['url'] = 'http://www.bhaskar.com' + news.xpath('div/a/@href').extract_first()
            item['img_title'] = news.xpath('div/a/@title').extract_first()
            if news.xpath('a/img/@src').extract_first():
                item['img_urls'] = news.xpath('a/img/@src').extract_first()
            else:
                item['img_urls'] = news.xpath('a/img/@data-original').extract_first()

            if item['url']:
                request = scrapy.Request(url=item['url'], callback=self.parse_detail_page, meta={'item':item}, dont_filter=True)   
            request.meta['item'] =item
            
            yield request

    def parse_detail_page(self, response):
        item = response.meta['item']
        detailPageSelector = Selector(response)
        item['shortdesc'] = item['description'] = detailPageSelector.xpath('//section[@class="db_storybox"]/h1').extract_first()

        
        yield item

