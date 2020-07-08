# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from pymongo import MongoClient


class HousespiderPipeline:
    def process_item(self, item, spider):
        return item


class LianjiaPipeline:
    def open_spider(self, spider):
        self.db = MongoClient(spider.settings.get("MONGODB_URL"))["houses"]

    def process_item(self, item, spider):
        if spider.name == "Lianjia":
            self.db[item['houseType']].insert(dict(item))

        return item
