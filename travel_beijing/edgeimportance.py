import numpy as np
import MySQLdb
import random
import math

conn=MySQLdb.connect(host='202.112.113.203',user='sxw',passwd='0845',port=3306,charset='utf8')
cur=conn.cursor()
conn.select_db('sns')
arr = np.zeros([167,167]) # all zero



    # print x, y
# print arr[0,0]
# print arr
#file_object = open('thefile.txt', 'wb+')


# file_object = open('x.txt', 'w')
# for i in range(1, 1001):
#     file_object.write(str(i)+" ")
# file_object.close()
for i in range(0,167):
    fromid=i+1
    for j in range(0,167):
        toid=j+1
        if fromid<>toid:
            cur.execute('select count(*) from edge where fromid='+str(fromid)+' and toid='+str(toid))
            from2to=cur.fetchone()[0]
            cur.execute('select count(*) from edge where fromid='+str(fromid))
            fromcount=cur.fetchone()[0]
            cur.execute('select count(*) from edge where fromid='+str(toid)+' and toid='+str(fromid))
            to2from=cur.fetchone()[0]
            cur.execute('select count(*) from edge where toid='+str(fromid))
            tocount=cur.fetchone()[0]
            cur.execute('select count(*) from edge')
            edgecount=cur.fetchone()[0]
            if fromcount!=0 and tocount!=0:
                fab=float(from2to)/fromcount
                dab=float(to2from)/tocount
                if (fab+dab)!=0 and from2to!=0:
                    Rab=(fab*dab)/(fab+dab)*math.log(from2to,math.e)/math.log(edgecount,math.e)
                    print 'insert into edgeimportance(fromid,toid,edgeimportance values('+str(fromid)+','+str(toid)+','+str(Rab)+')'
                    cur.execute('insert into edgeimportance(fromid,toid,edgeimportance) values('+str(fromid)+','+str(toid)+','+str(Rab)+')')



conn.commit()
cur.close()
conn.close()