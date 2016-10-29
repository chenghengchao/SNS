# -*- coding: utf-8 -*-

import math
from math import radians, cos, sin, asin, sqrt
import MySQLdb
from baidumap import BaiduMap
import os

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
    conn=MySQLdb.connect(host='202.112.113.203',user='sxw',passwd='0845',port=3306,charset='utf8')
    cur=conn.cursor()
    conn.select_db('atmo')

    sitelist=[]
    i=0
    #city='北京'.decode('ut')
    count1=cur.execute('select distinct(subsite) from atmo.weather where subsite<>site and city="北京"')
    results = cur.fetchall()
    count=cur.execute('SELECT * FROM atmo.location where lat <> 39.9299857780;')
    results1=cur.fetchall()
    for r in results:
        bdmap = BaiduMap("北京")
        if not '北京' in r[0]:
            site='北京'+r[0]
        print site
        site=site+'气象观测站'
        bd_point = bdmap.getLocation(site)
        if bd_point.find("lng")!=-1:
            index = bd_point.find('lng')
            lng=bd_point[index+5:index+18]
        if bd_point.find("lat")!=-1:
            index = bd_point.find('lat')
            lat=bd_point[index+5:index+18]

        print 'there has %s rows record' % count

        for r1 in results1:
            dis= haversine(float(lng),float(lat),float(r1[3]),float(r1[2]))
            angle1 = angle(float(lat),float(lng),float(r1[2]),float(r1[3]))
            factory=r1[1]
            if r1[3]>=lng and r1[2]>=lat:
                type='1'
                if angle1>=270:
                    flag='1'
                else:
                    flag='0'
            elif r1[3]<=lng and r1[2]>=lat:
                type='2'
                if angle1<=90 and angle1>=0:
                    flag='1'
                else:
                    flag='0'
            elif r1[3]<=lng and r1[2]<=lat:
                type='3'
                if angle1<=180 and angle1>=90:
                    flag='1'
                else:
                    flag='0'
            elif r1[3]>=lng and r1[2]<=lat:
                type='4'
                if angle1<=270 and angle1>=180:
                    flag='1'
                else:
                    flag='0'


            cur.execute('insert into atmo.siteangle(site,factory,distance,angle,type,flag,sitelat,sitelng,factorylat,factorylng) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',
                              (site,factory,str(dis),str(angle1),type,flag,str(lat),str(lng),str(r1[2]),str(r1[3])))


    conn.commit()
    cur.close()
    conn.close()











except MySQLdb.Error,e:
     print "Mysql Error %d: %s" % (e.args[0], e.args[1])