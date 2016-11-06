# -*- coding: utf-8 -*-
import pymongo
import MySQLdb

sqlconn=MySQLdb.connect(host='202.112.113.203',user='sxw',passwd='0845',port=3306,charset='utf8')
cur=sqlconn.cursor()
sqlconn.select_db('sns')

cur.execute('select id,name from modify_scenes_v1')
scenes=cur.fetchall()

mongoconn = pymongo.MongoClient('202.112.113.203',27017)
db = mongoconn['travel']
beijinginfo=db['travel_beijing']

#mongodb循环赌一次结束，每次需要重新抓取，mongodb中不是utf-8需要先
scenedegree={}
print scenes
for scene in scenes:
    name=scene[1].decode('utf-8').encode('utf-8')
    count=0
    all=beijinginfo.find().sort('title',-1)
    for one in all:
        path=one['modifypath'].encode('utf-8')
        #print name,path
        if name in path:
            count=count+1

    scenedegree[name]=count
    cur.execute('update modify_scenes_v1 set degree='+str(count)+' where id='+str(scene[0]))
    #print scenedegree


sqlconn.commit()
sqlconn.close()
cur.close()
mongoconn.close()
