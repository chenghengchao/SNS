# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TravelBeijingItem(scrapy.Item):
    # define the fields for your item here like:
    author = scrapy.Field()
    title = scrapy.Field()
    path = scrapy.Field()

