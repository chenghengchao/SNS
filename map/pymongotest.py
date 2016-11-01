# -*- coding: utf-8 -*-
import pymongo
import MySQLdb
import os
import re
import string

# 建立Mysql连接 返回connection
def getMySqlConn():
    sqlconn = MySQLdb.connect(host='202.112.113.203', user='sxw', passwd='0845', port=3306, charset='utf8')
    # cur = sqlconn.cursor()
    # sqlconn.select_db('sns')
    return sqlconn

# 建立MongoDb 连接，返回connection
def getMongoConn():
    conn = pymongo.MongoClient('202.112.113.203', 27017)
    # db = conn['travel']
    # beijingInfo = db['travel_beijing_detail']
    return conn

# 计算时间的平均值
def computeTime():
    connection = getMySqlConn()
    cur = connection.cursor()
    connection.select_db('sns')
    tempManyTime = cur.execute("select manytime,id from scenes")
    tempRes = cur.fetchall()
    for index, trs in enumerate(tempRes):
        if trs[0] <> None:
            timeList = trs[0]
            print timeList
            listLen = len(timeList)
            totaltime = 0
            count = 0
            for t1 in range(listLen):
                digit = timeList[t1]
                if digit.isdigit():
                    count = count + 1
                    totaltime += int(timeList[t1].strip())
            print totaltime

            avg = totaltime * 1.0 / count
            print avg
            print "------"
            # print "index: "+trs[1]
            cur.execute("update sns.scenes set oritime="+str(avg)+" where id ="+str(trs[1]))
    connection.commit()
    cur.close()
    connection.close()

# 从mongodb中读取时间，并存入mysql中sence表的manytime字段
def updateManyTime():
    conn = getMongoConn()
    db = conn['travel']
    beijingInfo = db['travel_beijing_detail']

    sqlconn = getMySqlConn()
    cur = sqlconn.cursor()
    sqlconn.select_db('sns')
    all = beijingInfo.find({'destination':u'北京'})

    sql = "select name from scenes"
    scenes = cur.execute(sql)
    scenesRs = cur.fetchall()
    sceneDict = {}
    for r in scenesRs:
        sceneDict[r[0]] = []
    count = 0
    for i in all:
        plan = i['plan']
        print i['title']
        count = count + 1
        for j, day in plan.items():
        # print j
            scene = day['day-scene']
            for m, t in scene.items():
                if 'scene-time' in t.keys():
                    tempTime = t['scene-time'].encode('utf-8')
                    tempName = t['scene-name'].encode('utf-8')
                    pattern = re.compile(r'\d')
                    if tempName in sceneDict.keys():

                        res = pattern.search(tempTime)
                        if res:
                        # theTime = float(res.group()[0])
                            theTime = res.group()[0]
                        # digitTime = float(theTime)
                            if '天' in tempTime:
                                theTime = str(theTime * 24)
                            # digitTime = theTime * 24
                            if len(theTime) > 1000:
                                theTime = theTime[:1000]
                            sceneDict[tempName].append(theTime)
                            cur.execute("update sns.scenes set manytime='" + ' '.join(sceneDict[tempName])+"' where name='"+ tempName+"'")
    print count
# for k, v in sceneDict.items():
#     print k, v

    sqlconn.commit()
    sqlconn.close()
    cur.close()
    conn.close()

# 将表scene的时间转换到modifyScene表
def transferTime():
    connection = getMySqlConn()
    cur = connection.cursor()
    connection.select_db('sns')
    oriTime = cur.execute("select oritime, modifyname from scenes")
    Rs = cur.fetchall()
    for r in Rs:
        if r[0] <> None and r[1] <> None:
            tmpTime = r[0]
            tmpname = r[1].decode('utf-8').encode('utf-8')
            print tmpTime, tmpname
            cur.execute("update modify_scenes set playtime =" + str(tmpTime)+" where name = '"+tmpname+"'")
    connection.commit()
    connection.close()

# main函数
if __name__ == '__main__':
    # computeTime()
    # transferTime()
    updateManyTime()



