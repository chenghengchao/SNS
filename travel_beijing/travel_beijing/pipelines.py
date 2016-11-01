# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from twisted.enterprise import adbapi
import MySQLdb
import MySQLdb.cursors
from scrapy.crawler import Settings as settings
import pymongo
from scrapy.conf import settings
import pymongo

class TravelBeijingPipeline(object):
    def __init__(self):
        host = settings['HOST']
        port = settings['PORT']
        dbName = settings['DB']
        client = pymongo.MongoClient(host=host, port=port)
        tdb = client[dbName]
        self.post = tdb[settings['COLLECTION']]


    def process_item(self, item, spider):
        travelInfo = dict(item)
        self.post.insert(travelInfo)
        return item

