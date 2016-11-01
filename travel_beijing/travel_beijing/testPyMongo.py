# -*- coding: utf-8 -*-

import pymongo
#from pymongo import Connection
conn = pymongo.MongoClient('202.112.113.203',27017)
db = conn['travel']
beijinginfo=db['travel_beijing']
#查询一条
#print beijinginfo.find_one({"title":"北京6日经典行程"})
#查询所有
all=beijinginfo.find().sort('title',-1)
for i in all:
    if u'流氓村' in i['path']:
        print i['path']
#条件查询
# some=beijinginfo.find({"title":"北京6日经典行程"})
# for i in some:
#     print i


