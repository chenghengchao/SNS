# -*- coding: utf-8 -*-
import MySQLdb
from baidumap import BaiduMap

sqlconn=MySQLdb.connect(host='202.112.113.203',user='sxw',passwd='0845',port=3306,charset='utf8')
cur=sqlconn.cursor()
sqlconn.select_db('sns')

cur.execute('select * from scenes')

all=cur.fetchall()

for one in all:
    id=one[0]
    scene=one[1]
    print 'select name from std_scenes where name="'+scene+'"'
    count=cur.execute('select name from std_scenes where name like "%'+scene+'%"')
    if count!=0:
        modifyname=cur.fetchone()[0]
        cur.execute('update scenes set modifyname="'+modifyname+'" where id='+str(id))


sqlconn.commit()
sqlconn.close()
cur.close()
