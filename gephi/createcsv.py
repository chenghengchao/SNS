# -*- coding: utf-8 -*-
import urllib2
import urllib
from bs4 import BeautifulSoup
import MySQLdb
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

def getedgedegree():
    conn = MySQLdb.connect(host='202.112.113.203', user='sxw', passwd='0845', port=3306, charset='utf8')
    cur = conn.cursor()
    conn.select_db('sns')
    cur.execute('select fromid,toid from edge')
    edges={}
    results=cur.fetchall()
    for one in results:
        path=str(one[0])+"-"+str(one[1])
        if path not in edges.keys():
            edges[path]=1
        else:
            edges[path]=edges[path]+1
    for key,item in edges.items():
        fromid=key.split('-')[0]
        toid=key.split('-')[1]
        degree=item
        cur.execute('insert into edges(fromid,toid,degree) values('+str(fromid)+','+str(toid)+','+str(degree)+')')

    conn.commit()
    cur.close()
    conn.close()

def createNodesAndEdges():
    conn = MySQLdb.connect(host='202.112.113.203', user='sxw', passwd='0845', port=3306, charset='utf8')
    cur = conn.cursor()
    conn.select_db('sns')
    f=open('Nodes.csv','wb+')
    f.write('id,Label,City,Longitude,Latitude\n')
    cur.execute('select id,name,reallat,reallng from modify_scenes_v1')
    results=cur.fetchall()
    for scene in results:
        id=scene[0]
        name=scene[1].decode('utf-8').encode('gbk')
        reallat=scene[2]
        reallng=scene[3]
        f.write(str(id)+','+name+',Beijing,'+str(reallng)+','+str(reallat)+'\n')

    f.close()
    f1=open('Edges.csv','wb+')
    f1.write('Source,Target,Type,Weight\n')
    cur.execute('select fromid,toid,degree from edges')
    results=cur.fetchall()
    for edge in results:
        fromid=edge[0]
        toid=edge[1]
        degree=edge[2]
        f1.write(str(fromid)+','+str(toid)+',Directed,'+str(degree)+'\n')
    f1.close()

#getedgedegree()
createNodesAndEdges()