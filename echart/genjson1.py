# -*- coding: utf-8 -*-
import urllib2
import cookielib
import MySQLdb
import os
import random

def getjson():
    #f=open('graph.json','wb+')
    conn = MySQLdb.connect(host='202.112.113.203', user='sxw', passwd='0845', port=3306, charset='utf8')
    cur = conn.cursor()
    conn.select_db('sns')
    # cur.execute("insert into sns.distance(fromid, toid, distance) values('%d', '%d', '%f')" % (tmplat + 1, tmplng + 1, float(distance)))
    cur.execute('select id,name,reallng,reallat,pagerank from modify_scenes_v1 order by pagerank desc')
    results=cur.fetchall()
    #{"nodes": [{"color": "#4f19c7", "label": "jquery", "attributes": {}, "y": -404.26147, "x": -739.36383, "id": "jquery", "size": 4.7252817}
    jsonstr='data: ['
    node=[]
    scenes={}
    colors=['#FF9912','#00FFFF','#00C957','#FF6100','#DA70D6','#F0FFF0']
    for one in results[30:45]:
        id=one[0]
        name=one[1]
        scenes[str(id)]=name
        lng=one[2]+random.random()*50
        lat=one[3]+random.random()*20
        pagerank=one[4]*300
        node.append(str(id))
        color=colors[int(random.random()*5)]

        onenode="{name: '"+name+"',x:"+str(lng)+" ,y: "+str(lat)+",symbolSize:100},"
        jsonstr=jsonstr+onenode
    nodes=','.join(node)
    jsonstr=jsonstr[:-1]+"], links: ["
    cur.execute('select fromid,toid,degree from edges where fromid in ('+nodes+') and toid in ('+nodes+')')
    #print 'select fromid,toid from distance where fromid in ('+nodes+') and toid in ('+nodes+')'
    results=cur.fetchall()
    #"sourceID": "jquery", "attributes": {}, "targetID": "htmlparser", "size": 1}
    for one in results:
        fromid=scenes[str(one[0])]
        toid=scenes[str(one[1])]
        value=one[2]
        oneedge="{source: '"+fromid+"',target: '"+toid+"',value:"+str(value)+",label: {normal: {show: true,formatter:'{c}'}},lineStyle: {normal: {curveness: 0.2}}},"
        jsonstr=jsonstr+oneedge
    jsonstr=jsonstr[:-1]+'],'

    print jsonstr
    #f.write(jsonstr.encode('utf-8'))
    cur.close()
    conn.close()


getjson()