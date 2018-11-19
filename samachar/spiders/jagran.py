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
        'https://www.jagran.com/feature-news-hindi.html',
    )

    def parse(self, response):
     
        news = Selector(response).xpath("//ul[@class='topicList']/li")
        print news
        for news in news:
            item = SamacharItem()
            item['title'] = news.xpath("a/div[@class='protxt fr']/div[@class='h3']/text()").extract_first()
            item['url'] = 'https://www.jagran.com' + news.xpath("a/@href").extract_first()

            if item['url']:
                request = scrapy.Request(url=item['url'], callback=self.parse_detail_page, meta={'item':item}, dont_filter=True)   
            request.meta['item'] =item
            yield request

    def parse_detail_page(self, response):
        item = response.meta['item']
        detailPageSelector = Selector(response)
        
        if detailPageSelector.xpath("//figure[@class='bodySummery']/figcaption/text()").extract_first():
            item['shortdesc'] = detailPageSelector.xpath("//figure[@class='bodySummery']/figcaption/text()").extract_first()
            item['description'] = detailPageSelector.xpath("//div[@class='articleBody']/p[2]").extract_first()
        else:
            item['shortdesc'] = detailPageSelector.xpath("//div[@id='topHeading']/h1/text()").extract_first()
            item['description'] = detailPageSelector.xpath("//div[@class='articleBody']/p/text()").extract_first()

        item['img_title'] = detailPageSelector.xpath("//ul[@id='output']/li/a/@title").extract_first()

        if detailPageSelector.xpath("//img[@id='jagran_image_id']/@src").extract_first():
            item['img_urls'] = detailPageSelector.xpath("//img[@id='jagran_image_id']/@src").extract_first()
        else:
            item['img_urls'] = detailPageSelector.xpath("//div[@class='lt-image']/img/@src").extract_first()
        
        yield item

