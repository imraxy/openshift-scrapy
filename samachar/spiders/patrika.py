# -*- coding: utf-8 -*-
import scrapy
import logging
import urlparse

from scrapy.spiders import Spider
from scrapy.selector import Selector
from samachar.items import SamacharItem
import re
import sys

class PatrikaSpider(scrapy.Spider):
    name = "patrika"
    allowed_domains = ["patrika.com"]
    start_urls = (
        'http://www.patrika.com/feature/duniya-ajab-gajab/',
    )

    def parse(self, response):
     
        news = Selector(response).xpath("//span[@class='list-con-heading']")
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
        
        if detailPageSelector.xpath("//div[@class='storyhead']/span/text()").extract_first():
            item['shortdesc'] = detailPageSelector.xpath("//div[@class='storyhead']/span/text()").extract_first()
            item['description'] = detailPageSelector.xpath("//div[@class='storyhead']/span/text()").extract_first()
        else:
            item['shortdesc'] = "No Description"
            item['description'] = "No Description"

        item['img_title'] = detailPageSelector.xpath("//img[@class='leadPic']/@alt").extract_first()

        if detailPageSelector.xpath("//img[@class='leadPic']/@src").extract_first():
            item['img_urls'] = detailPageSelector.xpath("//img[@class='leadPic']/@src").extract_first()
        else:
            item['img_urls'] = "No Image!"
        
        yield item

