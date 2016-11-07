#coding=utf-8

import MySQLdb
import csv

conn = MySQLdb.connect(host='202.112.113.203', user='sxw', passwd='0845', port=3306, charset='utf8')
cur = conn.cursor()
conn.select_db('sns')


csvfile = file('drivedistance.csv', 'rb+')
reader = csvfile.read()
lines=reader.split("\n")



for i in range(0,len(lines)):
    if lines[i]!="":
        line=lines[i]
        fromid=line.split(',')[0]
        toid=line.split(',')[1]
        distance=line.split(',')[2]
        print 'update sns.distance set drivedistance='+str(distance)+' where fromid='+str(fromid)+' and toid='+str(toid)
        cur.execute('update sns.distance set drivedistance='+str(distance)+' where fromid='+str(fromid)+' and toid='+str(toid))


conn.commit()
cur.close()
conn.close()
