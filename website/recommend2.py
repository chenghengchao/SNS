
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


#得到最新的路径
    def getallpath(self,curlist,cost=8,month="01"):
        removelist=[]
        conn = MySQLdb.connect(host='202.112.113.203', user='sxw', passwd='0845', port=3306, charset='utf8')
        cur = conn.cursor()
        conn.select_db('sns')
        for i in range(0,len(curlist)):
            flag=False
            path=curlist[i][1:]
            fromid=path[len(path)-1]
            cur.execute('select toid,edgecost from distance where distance<10 and fromid='+str(fromid)+' and besttime like "%'+month+'%" order by pagerank desc')
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

#景点去重，同时去掉时间花费
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

    def getmaximportant(self,tmpDict,allpath,totalcost):
        max = 0
        maxpath = ''
        code_path=''
        for i in allpath:
            path=[]
            pagerank=0
            cost=0

            for scene in i:

                path.append(tmpDict[scene][0])
                pagerank=pagerank+tmpDict[scene][2]
                cost=cost+tmpDict[scene][1]
            path='-->'.join(path)
            pagerank=pagerank/len(i)
            #print pagerank,cost,max
            if pagerank>max and cost<totalcost:
                max=pagerank
                maxpath=path
                code_path=i
        return maxpath,code_path


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


            cur.execute("select name,price,pagerank,modify_besttime,playtime from modify_scenes_v1 where id= " + str(fromid))
            tmpRs = cur.fetchall()
            for rs in tmpRs:
                price =rs[1]
                if len(price)>1:
                    price=int(price[:-2])
                else:
                    price=0
                pagerank=float(rs[2])
                besttime=rs[3]
                playtime=rs[4]

                fromNodeList[fromid]=[rs[0],price,pagerank,besttime,playtime]

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
            pathdict['pic'].append('../static/scene_img/'+str(detail[0])+'.jpg')
            pathdict['address'].append(detail[5])

        return pathdict
    #将得到的总路径分解
    def getdaypath(self,tmpDict,days,paths):
        print paths
        daypaths={0:[],1:[],2:[]}
        conn = MySQLdb.connect(host='202.112.113.203', user='sxw', passwd='0845', port=3306, charset='utf8')
        cur = conn.cursor()
        conn.select_db('sns')
        if days==1:
            for i in range(0,3):
                path=paths[i]
                daypath=[]
                for scene in path:
                    daypath.append(tmpDict[scene][0])
                daypaths[i].append('-->'.join(daypath))

        else:
            for i in range(0,3):
                codepath=paths[i]
                for day in range(1,days):
                    daypath=[]
                    cost=0
                    for t in range(len(codepath)-1):
                        fromid=codepath[t]
                        toid=codepath[t+1]
                        if cost==0:
                            cost=cost+tmpDict[fromid][4]
                            daypath.append(tmpDict[fromid][0])
                        cur.execute('select edgecost from distance where fromid='+str(fromid)+' and toid='+str(toid))
                        cost=cost+cur.fetchone()[0]
                        if cost<8:
                            daypath.append(tmpDict[fromid][0])
                    codepath=codepath[len(daypath):]
                    daypaths[i].append('-->'.join(daypath))
                daypath=[]
                for scene in codepath:
                    daypath.append(tmpDict[scene][0])
                daypaths[i].append('-->'.join(daypath))
        print daypaths
        return daypaths







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
        conn = MySQLdb.connect(host='202.112.113.203', user='sxw', passwd='0845', port=3306, charset='utf8')
        cur = conn.cursor()
        conn.select_db('sns')
        cur.execute('select id,name,playtime from modify_scenes_v1 where modify_besttime like "%'+month+'%" order by pagerank desc ')
        result=cur.fetchmany(3)

        cur.close()
        conn.close()
        tmpDict = self.getDataFromDb()
        print tmpDict
        paths=[]
        code_paths=[]
        for one in result:
            allpath=[[one[2],one[0]]]
            flag=True
            temp=allpath
            while flag:
                allpath,flag=self.getallpath(temp,days*8,month)

                temp=allpath


            allpath=self.duplicatepath(allpath)
            #mincostpath,mincost=self.getmincost(tmpDict,allpath)
            maximportantpath,code_path=self.getmaximportant(tmpDict,allpath,cost)


            print maximportantpath,code_path
            paths.append(maximportantpath)
            code_paths.append(code_path)
        path_by_day=self.getdaypath(tmpDict,days,code_paths)
        print path_by_day
        return paths,path_by_day

        #dateupdate()



