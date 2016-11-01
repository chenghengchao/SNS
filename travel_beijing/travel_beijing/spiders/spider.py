# -*- coding: utf-8 -*-

import scrapy
import string
import time
import datetime
import json
import urllib2
import os
import re
from travel_beijing.items import TravelBeijingItem
import cookielib
from pinyin import PinYin



class WeatehrSpider(scrapy.spiders.Spider):
    name = "travel"
    allowed_domains = ["lvyou.baidu.com"]
    start_urls = [
        "https://lvyou.baidu.com/plan/counselor?surls[]=beijing&days_cnt_low=&days_cnt_high=&pn=0&rn=30" ]

    #//*[@id="J_is-good"]/div[2]/div[2]/ul[2]/li[2]/ul[2]/li[1]/a,,//*[@id="J_is-good"]/div[2]/div[2]/ul[2]/li[2]/ul[2]/li[3]/a[3]
    #//*[@id="J_is-good"]/div[2]/div[2]/ul[2]/li[2]/ul[4]/li[1]/a[1],//*[@id="J_is-good"]/div[2]/div[2]/ul[2]/li[2]/ul[3]/li[1]/a[1]
    #//*[@id="J_is-good"]/div[2]/div[2]/ul[2]/li[3]/ul[6]/li/a


    def parse(self, response):
        print len(response.xpath('//li[@class="list-item"]').extract())+1
        for i in range(1,len(response.xpath('//li[@class="list-item"]').extract())+1):
            author=''.join(response.xpath('//li[@class="list-item"]['+str(i)+']/div[@class="author-info"]/div/a[2]/text()').extract())
            title=''.join(response.xpath('//li[@class="list-item"]['+str(i)+']/div[@class="plan-info"]/a[1]/text()').extract())
            timecount=''.join(response.xpath('//li[@class="list-item"]['+str(i)+']/div[@class="plan-info"]/p[class="plan-trip-day"]/text()').extract())
            url='http://lvyou.baidu.com'+''.join(response.xpath('//li[@class="list-item"]['+str(i)+']/a[1]/@href').extract())
            yield scrapy.Request(url,meta={'author':author,'title':title,'timecount':timecount},callback=self.parse3)

        for i in range(1,26):
            url='https://lvyou.baidu.com/plan/counselor?surls[]=beijing&days_cnt_low=&days_cnt_high=&pn='+str(i*30)+'&rn=30'
            yield scrapy.Request(url,callback=self.parse2)



    def parse2(self,response):
        print len(response.xpath('//li[@class="list-item"]').extract())+1
        for i in range(1,len(response.xpath('//li[@class="list-item"]').extract())+1):
            author=''.join(response.xpath('//li[@class="list-item"]['+str(i)+']/div[@class="author-info"]/div/a[2]/text()').extract())
            title=''.join(response.xpath('//li[@class="list-item"]['+str(i)+']/div[@class="plan-info"]/a[1]/text()').extract())
            timecount=''.join(response.xpath('//li[@class="list-item"]['+str(i)+']/div[@class="plan-info"]/p[class="plan-trip-day"]/text()').extract())
            url='http://lvyou.baidu.com'+''.join(response.xpath('//li[@class="list-item"]['+str(i)+']/a[1]/@href').extract())
            yield scrapy.Request(url,meta={'author':author,'title':title,'timecount':timecount},callback=self.parse3)


    #//*[@id="plan-trip-detail"]/div[1]/section[1]
    def parse3(self,response):
        #file_object = open('thefile.txt', 'w+')
        item=TravelBeijingItem()
        #response.meta['destination'],
        item['author']=''.join(response.meta['author'])
        item['title']=''.join(response.meta['title'])

#//*[@id="plan-trip-path"]
        #//*[@id="day-path-54125e395a3f99135f7a357f"]/header/div/a
        #//*[@id="day-path-54125e395a3f99135f7a357f"]/header/div/span/a[1]
        path=''
        pathcount=len(response.xpath('//div[@id="plan-trip-path"]/div[1]/section'))


        for i in range(1,pathcount+1):
            scenecount=len(response.xpath('//div[@id="plan-trip-path"]/div[1]/section['+str(i)+']/header/div/span/a'))
            for j in range(1,scenecount+1):
                path=path+''.join(response.xpath('//div[@id="plan-trip-path"]/div[1]/section['+str(i)+']/header/div/span/a['+str(j)+']/text()').extract())+'-'
        item['path']=path
        yield item







































