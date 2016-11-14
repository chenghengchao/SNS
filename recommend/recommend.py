# -*- coding: utf-8 -*-

import numpy as np
import MySQLdb

def isequal(a, b):
    '''判断两个数组是否相等'''
    if len(a) != len(b):
        return False
    else:
        m, n = np.shape(a)
        # l, k = np.shape(b)
        # print m, n
        # print l, k
        for i in range(m):
            if len(a[i]) != len(b[i]):
                return False
            else:
                for j in range(n):

                    # print a[i][j]
                    # print '-' * 8
                    # print b[i][j]

                    if a[i][j] != b[i][j]:
                        return False
                    else:
                        continue
        return True


def getAllPath(fromid, cost=8):
    paths = set()
    path = str(fromid)
    tmpDict = getDataFromDb()
    tmpList = tmpDict[fromid]
    # print tmpList
    if len(tmpList) == 1:
        # print "0"
        path = str(fromid) + '-->' + str(tmpList[0][0])
        # print path
        paths.add(path)
    else:
        for tp in tmpList:
            # if len(tmpList) == 1:
            #     print str(fromid) + '-->' + str(tp[0])
            #     return str(fromid) + '-->' + str(tp[0])
            curCost = 0
            path = path + '-->' + str(tp[0])

            curCost = curCost + tp[1]
            if curCost > cost:
                # if tp[0] == 167
                # print "1"
                # print path
                paths.add(path)
                # return path
            elif tp[0] == 167:
                # print "2"
                # print path
                paths.add(path)
                # return
            else:
                getAllPath(tp[0])
    # print "set start"
    # print paths
    return paths

    # class Node:
    #     fromNode = ""
    #     toNode = ""
    #     allNode = []
    #
    #     def __init__(self, fromNode, toNode):
    #         self.fromNode = fromNode
    #         self.toNode = toNode
    #
    #     def getAllNode(self, Node):
    #         sql = "select from, to from table"


def getDataFromDb():
    conn = MySQLdb.connect(host='202.112.113.203', user='sxw', passwd='0845', port=3306, charset='utf8')
    cur = conn.cursor()
    conn.select_db('sns')
    # cur.execute("insert into sns.distance(fromid, toid, distance) values('%d', '%d', '%f')" % (tmplat + 1, tmplng + 1, float(distance)))
    # cur.execute("insert into sns.scenes_list(name, url, grade, price, guide, address, special) VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s')" % (name, url, grade, price, guide, address, spe))
    cur.execute("select fromid, toid, edgecost from distance ")
    result = cur.fetchall()
    fromNodeList = {}
    costList = {}
    for res in result:
        fromid = res[0]
        tmpList = []
        tolist = []
        fromNodeList[fromid] = []

        cur.execute("select toid, edgecost from distance where fromid = " + str(fromid))
        tmpRs = cur.fetchall()
        for rs in tmpRs:
            tmp = (int(rs[0]), float(rs[1]))
            tolist.append(tmp)
            fromNodeList[fromid].append(tmp)

    # for i, j in fromNodeList.items():
    #     print i, j
    return fromNodeList

    conn.commit()
    cur.close()
    conn.close()




if __name__ == '__main__':
    #
    # a = [[1, 2, 3], [4, 5, 6]]
    # b = [[1, 2, 3], [4, 5, 6]]
    # c = [[1, 2, 3], [4, 5, 7]]
    # d = [[1, 2, 3], [4, 5]]
    # e = [[1, 2], [4, 5, 3]]
    # print isequal(a, b)
    # print isequal(a, c)
    # print isequal(a, d)
    # print isequal(a, e)
    # getDataFromDb()

    print getAllPath(1)



