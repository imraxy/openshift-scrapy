# -*- coding: utf-8 -*-
import scrapy
import logging
import urllib.parse

from scrapy.spiders import Spider
from scrapy.selector import Selector
from samachar.items import SamacharItem
import re
import sys


class PatrikaSpider(scrapy.Spider):
    name = "patrika"
    allowed_domains = ["patrika.com"]
    start_urls = (
        'https://www.patrika.com/weird-news/',
    )

    def parse(self, response):

        news = Selector(response).xpath(
            "//figcaption[@class='figure-caption']")
        print(news)
        for news in news:
            item = SamacharItem()
            item['title'] = news.xpath("a/span/text()").extract_first()
            item['url'] = news.xpath("a/@href").extract_first()

            if item['url']:
                request = scrapy.Request(url=item['url'], callback=self.parse_detail_page, meta={
                                         'item': item}, dont_filter=True)
            request.meta['item'] = item
            yield request

    def parse_detail_page(self, response):
        item = response.meta['item']
        detailPageSelector = Selector(response)

        if detailPageSelector.xpath("//div[@class='story-heading pos-relative orig-story']/h1/text()").extract_first():
            item['shortdesc'] = detailPageSelector.xpath(
                "//div[@class='story-heading pos-relative orig-story']/h1/text()").extract_first()
            item['description'] = detailPageSelector.xpath(
                "//div[@class='story-heading pos-relative orig-story']/h1/text()").extract_first()
        else:
            item['shortdesc'] = "No Description"
            item['description'] = "No Description"

        item['img_title'] = detailPageSelector.xpath(
            "//div[@id='image-video-section']/img/@alt").extract_first()

        if detailPageSelector.xpath("//div[@id='image-video-section']/img/@src").extract_first():
            item['img_urls'] = detailPageSelector.xpath(
                "//div[@id='image-video-section']/img/@src").extract_first()
        else:
            item['img_urls'] = "No Image!"

        yield item
