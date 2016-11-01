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
    scenes=i['path'][:-1].split('-')
    for j in range(0,len(scenes)):
        count=cur.execute('select modifyname from scenes where name="'+scenes[j]+'"')
        if count==0:
            scenes[j]="-"
        else:
            scenes[j]=cur.fetchone()[0]
    while '-' in scenes:
        scenes.remove('-')
    newpath='-'.join(scenes)
    print newpath
    beijinginfo.update({'_id':i['_id']},{"$set":{"modifypath":newpath}})


sqlconn.commit()
sqlconn.close()
cur.close()
mongoconn.close()
