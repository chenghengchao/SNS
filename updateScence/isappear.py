import MySQLdb
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

def isAppear():
    conn = MySQLdb.connect(host='202.112.113.203', user='sxw', passwd='0845', port=3306, charset='utf8')
    cur = conn.cursor()
    conn.select_db('sns')
    cur.execute("select name from modify_scenes_v1")
    result1 = cur.fetchall()

            # for res in result1:
            #     name = res[0]
            #     count = cur.execute("select name from scenes_list where name ='"+name+"'")
            #     # print count
            #     if count > 0:
            #         print "1111111111"
            #         cur.execute("update modify_scenes_v1 set isappear = 1 where name ='" + name + "'")
    cur.execute("select name from scenes_list")
    result2 = cur.fetchall()
    r2 = []
    for res2 in result2:
        r2.append('u'+res2[0])
    # print r2

    print  "------"*5
    r1 = []
    for res1 in result1:
        # print res1[0]
        r1.append(res1[0])
    # print r1

    print  "------"*5
    cross = []
    for i in r1:
        name = i.decode('utf-8').encode('utf-8')
        # print name
        # print i
        for j in r2:
            name2 = j.decode('utf-8').encode('utf-8')
            name2 = name2[1:]
            # print j
            # print name2
            if name == name2:
            # if i == j:
                cross.append(name)
        # print '*'*8
    # print cross
    print len(cross)
    for c in cross:
        # print c.decode('utf-8').encode('utf-8')
        cur.execute("update modify_scenes_v1 set isappear2 = 1 where name ='" + c + "'")

    conn.commit()
    cur.close()
    conn.close()

def updatedb():
    conn = MySQLdb.connect(host='202.112.113.203', user='sxw', passwd='0845', port=3306, charset='utf8')
    cur = conn.cursor()
    conn.select_db('sns')
    scenedict={}
    cur.execute('select id,modify_besttime from modify_scenes_v1')
    results=cur.fetchall()
    for one in results:
        scenedict[one[0]]=one[1]
    cur.execute('select id,toid from distance')
    results=cur.fetchall()
    for one in results:
        cur.execute('update distance set besttime="'+scenedict[one[1]]+'" where id='+str(one[0]))
    conn.commit()
    cur.close()
    conn.close()


if __name__ == '__main__':
    updatedb()