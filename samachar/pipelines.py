# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


# class SamacharPipeline(object):
#     def process_item(self, item, spider):
#         return item

import pymongo
import logging

#from scrapy.conf import settings
from scrapy.utils.project import get_project_settings
settings = get_project_settings()
from scrapy.exceptions import DropItem


class MongoDBPipeline(object):

    def __init__(self):
        connection = pymongo.MongoClient(
            settings['MONGODB_URI'],
        )

        db = connection[settings['MONGODB_DB']]
        self.collection = db[settings['MONGODB_COLLECTION']]

    def process_item(self, item, spider):

        if item['title']:
            item['title'] = item['title'].strip()

        if item['url']:
            item['url'] = item['url'].strip()

        if item['img_urls']:
            item['img_urls'] = item['img_urls'].strip()

        if item['img_title']:
            item['img_title'] = item['img_title'].strip()

        if item['shortdesc']:
            item['shortdesc'] = item['shortdesc'].strip()

        if item['description']:
            item['description'] = item['description'].strip()

        print("in process_item method")
        valid = True
        for data in item:
            if not data:
                valid = False
                raise DropItem("Missing {0}!".format(data))
        if valid:
            try:
                # self.collection.insert(dict(item))
                self.collection.update(
                    {"url": item['url']}, dict(item), upsert=True)
                logging.log(logging.DEBUG, "News added to MongoDB database!")

            except pymongo.errors.DuplicateKeyError:
                pass
        return item
