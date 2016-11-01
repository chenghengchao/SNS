# -*- coding: utf-8 -*-
import MySQLdb
from baidumap import BaiduMap

sqlconn=MySQLdb.connect(host='202.112.113.203',user='sxw',passwd='0845',port=3306,charset='utf8')
cur=sqlconn.cursor()
sqlconn.select_db('sns')

cur.execute('select * from modify_scenes')

all=cur.fetchall()
bdmap = BaiduMap("北京")
for one in all:
    scene=one[1]
    id=one[0]
    if not '北京' in scene:
        scene='北京'+scene
    bd_point = bdmap.getLocation(scene)
    if bd_point.find("lng")!=-1:
        index = bd_point.find('lng')
        lng=bd_point[index+5:index+18]
    if bd_point.find("lat")!=-1:
        index = bd_point.find('lat')
        lat=bd_point[index+5:index+18]
    lat=(float(lat)-39.9536402287)*100
    lng=(float(lng)-116.432188476)*100
    cur.execute('update modify_scenes set lat='+str(lat)+',lng='+str(lng)+' where id='+str(id))


sqlconn.commit()
sqlconn.close()
cur.close()
