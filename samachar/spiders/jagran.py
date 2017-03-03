# -*- coding: utf-8 -*-
import scrapy
import logging
import urlparse

from scrapy.spiders import Spider
from scrapy.selector import Selector
from samachar.items import SamacharItem
import re
import sys

class JagranSpider(scrapy.Spider):
    name = "jagran"
    allowed_domains = ["jagran.com"]
    start_urls = (
        'http://www.jagran.com',
    )

    def parse(self, response):
     
        news = Selector(response).xpath("//ul[@class='jagran-vishesh-list']/li")
        print news
        for news in news:
            item = SamacharItem()
            item['title'] = news.xpath("a/text()").extract_first()
            item['url'] = news.xpath("a/@href").extract_first()

            if item['url']:
                request = scrapy.Request(url=item['url'], callback=self.parse_detail_page, meta={'item':item}, dont_filter=True)   
            request.meta['item'] =item
            yield request

    def parse_detail_page(self, response):
        item = response.meta['item']
        detailPageSelector = Selector(response)
        
        if detailPageSelector.xpath("//ul[@id='output']/li/div/p/text()").extract_first():
            item['shortdesc'] = detailPageSelector.xpath("//ul[@id='output']/li/div/p/text()").extract_first()
            item['description'] = detailPageSelector.xpath("//ul[@id='output']/li/div/p/text()").extract_first()
        else:
            item['shortdesc'] = detailPageSelector.xpath("//div[@class='lt-image']/p/text()").extract_first()
            item['description'] = detailPageSelector.xpath("//div[@class='lt-image']/p/text()").extract_first()

        item['img_title'] = detailPageSelector.xpath("//ul[@id='output']/li/a/@title").extract_first()

        if detailPageSelector.xpath("//ul[@id='output']/li/a/img/@src").extract_first():
            item['img_urls'] = detailPageSelector.xpath("//ul[@id='output']/li/a/img/@src").extract_first()
        else:
            item['img_urls'] = detailPageSelector.xpath("//div[@class='lt-image']/img/@src").extract_first()
        
        yield item

