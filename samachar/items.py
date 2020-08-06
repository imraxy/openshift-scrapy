# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SamacharItem(scrapy.Item):
    # define the fields for your item here like:
    #name = scrapy.Field()
    title = scrapy.Field()
    url = scrapy.Field()
    img_urls = scrapy.Field()
    img_title = scrapy.Field()
    shortdesc = scrapy.Field()
    description = scrapy.Field()
    pass
