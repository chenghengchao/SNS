
# -*- coding: utf-8 -*-

import numpy as np
import MySQLdb

class recommend:

    def __init__(self):
        print 'hello'

    def isequal(self,a, b):
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


    # def getAllPath(tmpDict,fromid, cost=8):
    #     paths = set()
    #     path = str(fromid)
    #
    #     tmpList = tmpDict[fromid]
    #     # print tmpList
    #     if len(tmpList) == 1:
    #         # print "0"
    #         path = str(fromid) + '-->' + str(tmpList[0][0])
    #         # print path
    #         paths.add(path)
    #     else:
    #         for tp in tmpList:
    #             # if len(tmpList) == 1:
    #             #     print str(fromid) + '-->' + str(tp[0])
    #             #     return str(fromid) + '-->' + str(tp[0])
    #             curCost = 0
    #             path = path + '-->' + str(tp[0])
    #
    #             curCost = curCost + tp[1]
    #             if curCost > cost:
    #                 # if tp[0] == 167
    #                 # print "1"
    #                 # print path
    #                 paths.add(path)
    #                 # return path
    #             elif tp[0] == 167:
    #                 # print "2"
    #                 # print path
    #                 paths.add(path)
    #                 # return
    #             else:
    #                 getAllPath(tmpDict,tp[0])
    #     # print "set start"
    #     # print paths
    #     return paths

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
    def dateupdate(self):
        conn = MySQLdb.connect(host='202.112.113.203', user='sxw', passwd='0845', port=3306, charset='utf8')
        cur = conn.cursor()
        conn.select_db('sns')
        cur.execute('select id,fromid,toid,distance,edgecost from distance where distance<5')
        result=cur.fetchall()
        for one in result:
            cur.execute('insert into distance(fromid,toid,distance,edgecost) values('+str(one[2])+','+str(one[1])+','+str(one[3])+','+str(one[4])+')')
        conn.commit()
        cur.close()
        conn.close()



    def getallpath(self,curlist,cost=8):
        removelist=[]
        conn = MySQLdb.connect(host='202.112.113.203', user='sxw', passwd='0845', port=3306, charset='utf8')
        cur = conn.cursor()
        conn.select_db('sns')
        for i in range(0,len(curlist)):
            flag=False
            path=curlist[i][1:]
            fromid=path[len(path)-1]
            cur.execute('select toid,edgecost from distance where distance<5 and fromid='+str(fromid)+' order by pagerank desc')
            edges=cur.fetchmany(5)
            for edge in edges:
                if not edge[0] in path and (curlist[i][0]+edge[1])<cost:
                    curlist.append([curlist[i][0]+edge[1]]+path+[int(edge[0])])
                    flag=True
            if flag:
                removelist.append(i)

        print len(removelist)
        print len(curlist)
        i=len(removelist)-1
        while i>=0:
            curlist.remove(curlist[removelist[i]])
            i=i-1

        if removelist==[]:
            return curlist,False
        else:
            return curlist,True


    def duplicatepath(self,allpath):
        for i in range(0,len(allpath)):
            allpath[i]=allpath[i][1:]
        print type(allpath)

        tmpset=[]
        newpath=[]
        for i in allpath:
            subset=set(i)
            if not subset in tmpset:
                tmpset.append(subset)
                newpath.append(i)
        return newpath

    def getmincost(self,tmpDict,allpath):
        for i in allpath:
            path=[]
            min=100000
            cost=0
            minpath=''
            for scene in i:

                path.append(tmpDict[scene][0])
                cost=cost+tmpDict[scene][1]
            path='-->'.join(path)

            if cost<min:
                min=cost
                minpath=path
        return minpath,min

    def getmaximportant(self,tmpDict,allpath):
        for i in allpath:
            path=[]
            max=0
            cost=0
            maxpath=''
            for scene in i:

                path.append(tmpDict[scene][0])
                cost=cost+tmpDict[scene][2]
            path='-->'.join(path)
            cost=cost/len(i)
            print cost
            if cost>max:
                max=cost
                maxpath=path
        return maxpath


    def getDataFromDb(self):
        conn = MySQLdb.connect(host='202.112.113.203', user='sxw', passwd='0845', port=3306, charset='utf8')
        cur = conn.cursor()
        conn.select_db('sns')
        # cur.execute("insert into sns.distance(fromid, toid, distance) values('%d', '%d', '%f')" % (tmplat + 1, tmplng + 1, float(distance)))
        # cur.execute("insert into sns.scenes_list(name, url, grade, price, guide, address, special) VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s')" % (name, url, grade, price, guide, address, spe))
        #cur.execute("select fromid, toid, edgecost from distance ")
        cur.execute("select distinct(fromid) from distance ")
        result = cur.fetchall()
        fromNodeList = {}
        costList = {}
        for res in result:
            fromid = res[0]


            cur.execute("select name,price,pagerank from modify_scenes_v1 where id= " + str(fromid))
            tmpRs = cur.fetchall()
            for rs in tmpRs:
                price =rs[1]
                if len(price)>1:
                    price=int(price[:-2])
                else:
                    price=0
                pagerank=float(rs[2])

                fromNodeList[fromid]=[rs[0],price,pagerank]

        # for i, j in fromNodeList.items():
        #     print i, j
        return fromNodeList

        conn.commit()
        cur.close()
        conn.close()


    def showdetail(self,path):
        conn = MySQLdb.connect(host='202.112.113.203', user='sxw', passwd='0845', port=3306, charset='utf8')
        cur = conn.cursor()
        conn.select_db('sns')
        scenes=path.split('-->')
        pathdict={"name":[],"price":[],"intro":[],"pic":[],"special":[],"address":[]}
        for scene in scenes:
            pathdict["name"].append(scene)
            cur.execute('select id,name,price,guide,special,address from modify_scenes_v1 where name="'+scene+'"')
            detail=cur.fetchone()
            pathdict["price"].append(detail[2])
            pathdict["intro"].append(detail[3][5:])
            pathdict["special"].append(detail[4])
            pathdict['pic'].append('../scene_img/'+str(detail[0])+'.jpg')
            pathdict['address'].append(detail[5])

        return pathdict


    def start(self,days,cost,month):
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
        tmpDict = self.getDataFromDb()
        print tmpDict
        allpath=[[2,6]]
        flag=True
        temp=allpath
        while flag:
            allpath,flag=self.getallpath(temp,days*8)

            temp=allpath


        allpath=self.duplicatepath(allpath)
        mincostpath,mincost=self.getmincost(tmpDict,allpath)
        maximportantpath=self.getmaximportant(tmpDict,allpath)

        print mincostpath
        print maximportantpath
        return maximportantpath

        #dateupdate()



