# -*- coding: utf-8 -*-
import pymongo
import MySQLdb
#from pymongo import Connection
mongoconn = pymongo.MongoClient('202.112.113.203',27017)
db = mongoconn['travel']
beijinginfo=db['travel_beijing']

sqlconn=MySQLdb.connect(host='202.112.113.203',user='sxw',passwd='0845',port=3306,charset='utf8')
cur=sqlconn.cursor()
sqlconn.select_db('sns')
all=beijinginfo.find().sort('title',-1)
for i in all:
    scenes=i['modifypath'].split('-')
    for j in range(0,len(scenes)):
        print 'select * from modify_scenes_v1 where name="'+scenes[j]+'"'
        count=cur.execute('select * from modify_scenes_v1 where name="'+scenes[j]+'"')
        if count==0 and scenes[j]!='':
            cur.execute('insert into modify_scenes_v1(name) values("'+scenes[j]+'")')


sqlconn.commit()
sqlconn.close()
cur.close()
mongoconn.close()
