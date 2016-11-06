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
f=open('graph.txt','wb+')
id=1
for i in all:
    scenes=i['modifypath'].split('-')
    j=0
    while j<len(scenes)-1:
        nowindex=j
        fromnode=scenes[nowindex]
        tonode=scenes[nowindex+1]
        while tonode==fromnode:
            nowindex=nowindex+1
            if nowindex+1>len(scenes)-1:
                break
            tonode=scenes[nowindex+1]
        if fromnode!=tonode and fromnode!='' and tonode!='':
            print id,fromnode,tonode
            cur.execute('select * from modify_scenes_v1 where name="'+fromnode+'"')
            fromid=cur.fetchone()[0]
            cur.execute('select * from modify_scenes_v1 where name="'+tonode+'"')
            toid=cur.fetchone()[0]
            f.write(str(fromid)+' '+str(toid)+'\n')
            cur.execute('insert into edge(fromid,toid) values('+str(fromid)+','+str(toid)+')')
        if nowindex+1>len(scenes)-1:
            break
        j=nowindex+1
    id=id+1

f.close()

sqlconn.commit()
sqlconn.close()
cur.close()
mongoconn.close()