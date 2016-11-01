# -*- coding: utf-8 -*-
import numpy as np
import MySQLdb

conn=MySQLdb.connect(host='202.112.113.203',user='sxw',passwd='0845',port=3306,charset='utf8')
cur=conn.cursor()
conn.select_db('sns')
arr = np.zeros([191,191])
file=open('ucinetfile.txt','wb+')
file.write('dl nr=191,nc=191')
file.write('\n')
file.write('col labels:')
file.write('\n')

for i in range(1,192):
    cur.execute('select name from modify_scenes where id='+str(i))
    nodeid=cur.fetchone()[0]
    file.write(str(i))
    if i!=191:
        file.write(",")
file.write('\n')
file.write('\ndata: \n')


for line in open('graph.txt'):
    if '#' in line:
        continue
    temp = line.split(" ")
    x = int(temp[0])
    y = int(temp[1])

    arr[x-1, y-1] = arr[x-1, y-1]+1
    # print x, y
# print arr[0,0]
# print arr
#file_object = open('thefile.txt', 'wb+')
for i in range(len(arr)):
    oneline=''
    for j in range(len(arr[i])):
        oneline=oneline+str(arr[i][j])[0]+" "
    file.write(oneline)
    file.write("\n")
file.close()

# file_object = open('x.txt', 'w')
# for i in range(1, 1001):
#     file_object.write(str(i)+" ")
# file_object.close()
cur.close()
conn.close()