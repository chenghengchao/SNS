# -*- coding: utf-8 -*-
import math
from math import radians, cos, sin, asin, sqrt
import MySQLdb
from baidumap import BaiduMap
import os
import sys

# 填充distance表中的距离，运行前需要先清空distance表
# sys.setdefaultencoding('utf-8')
# reload sys

def angle(lat1,lng1,lat2,lng2):

    y = math.sin(lng2-lng1) * math.cos(lat2)
    x = math.cos(lat1)*math.sin(lat2) - math.sin(lat1)*math.cos(lat2)*math.cos(lng2-lng1)
    brng = math.atan2(y, x)
    brng = math.degrees(brng)

    if(brng < 0):
        brng = brng +360;
    return brng;


def haversine(lon1, lat1, lon2, lat2):
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    r = 6371.1
    return c * r

try:
    conn = MySQLdb.connect(host='202.112.113.203', user='sxw', passwd='0845', port=3306, charset='utf8')
    cur = conn.cursor()
    conn.select_db('sns')

    i=0
    #city='北京'.decode('ut')
    scenes = cur.execute('select name from sns.modify_scenes_v1')
    results = cur.fetchall()
    # count=cur.execute('SELECT * FROM atmo.location where lat <> 39.9299857780;')
    # results1=cur.fetchall()
    temp = []
    for i, r in enumerate(results):
        # print r[0].decode('utf-8').encode('utf-8')
        # if i == 2:
        #     break
        temp.append(r[0])
    # print temp
    lnglist = []
    latlist = []
    for ind, i in enumerate(temp):
        # if i == 2: break
        location = i.decode('utf-8').encode('utf-8')
        print location
        bdmap = BaiduMap("北京")
        if '北京' not  in location:
            location = '北京' + location
        bd_point = bdmap.getLocation(location)
        # print bd_point
        if bd_point.find("lng") != -1:
            index = bd_point.find('lng')
            lng = bd_point[index + 5:index + 18]
            # print "lng:" + lng
            lnglist.append(float(lng))
        if bd_point.find("lat") != -1:
            index = bd_point.find('lat')
            lat = bd_point[index + 5:index + 18]
            # print "lng:" +lat
            latlist.append(float(lat))
        # cur.execute("insert into sns.modify_scenes(reallng,reallat) values('%f','%f')" % (float(lng), float(lat)))
        cur.execute("update sns.modify_scenes_v1 set reallng = "+str(lng) +"where id = "+str(ind+1))
        cur.execute("update sns.modify_scenes_v1 set reallat = "+str(lat) +"where id = "+str(ind+1))
    conn.commit()
    # os._exit(0)
    # 先测试前两个
    # print "lnglist:"
    # print lnglist
    # print "latlist:"
    # print latlist
    length = range(len(latlist))
    for tmplat in length:
        for tmplng in length:
            if tmplng > tmplat:
                distance = haversine(latlist[tmplat], lnglist[tmplat], latlist[tmplng], lnglist[tmplng])
    # print "distance:"
                print distance
                # cur.execute("truncate table sns.distance")
                cur.execute("insert into sns.distance(fromid, toid, distance) values('%d', '%d', '%f')" % (tmplat+1, tmplng+1, float(distance)))
    # os._exit(0)
    conn.commit()

    #         cur.execute('insert into atmo.siteangle(site,factory,distance,angle,type,flag,sitelat,sitelng,factorylat,factorylng) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',
    #                           (site,factory,str(dis),str(angle1),type,flag,str(lat),str(lng),str(r1[2]),str(r1[3])))
    cur.close()
    conn.close()
except MySQLdb.Error,e:
     print "Mysql Error %d: %s" % (e.args[0], e.args[1])