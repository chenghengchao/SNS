# -*- coding: utf-8 -*-

import scrapy
import string
import re
import os
import urllib2
import time
import json
import datetime
import MySQLdb
import sys
reload(sys)
sys.setdefaultencoding('utf8')

conn=MySQLdb.connect(host='202.112.113.203',user='sxw',passwd='0845',port=3306,charset='utf8')
cur=conn.cursor()
conn.select_db('sns')


cur.execute('select sum(degree) from modify_scenes_v1')
degreecount=cur.fetchone()[0]
print degreecount
cur.execute('select id,degree from modify_scenes_v1')
scenes=cur.fetchall()
for scene in scenes:
    degree=scene[1]
    #print degree
    nodeimportance=degree/float(degreecount)
    print nodeimportance
    cur.execute('update modify_scenes_v1 set nodeimportance='+str(nodeimportance)+' where id='+str(scene[0]))
conn.commit()



cur.close()
conn.close()
