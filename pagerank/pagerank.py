# -*- coding: utf-8 -*-
import os
import networkx as nx
import MySQLdb
import matplotlib.pyplot as plt
# os.chdir('C:\\Users\\XXX\\Desktop\\')

def getMySqlConn():
    '''获得数据库连接并返回'''
    sqlconn = MySQLdb.connect(host='202.112.113.203', user='sxw', passwd='0845', port=3306, charset='utf8')
    # cur = sqlconn.cursor()
    # sqlconn.select_db('sns')
    return sqlconn


def getNodeWeight():
    '''读取数据库获得节点的权重，返回nodeImportance：dict{id:weight}'''
    conn = getMySqlConn()
    cur = conn.cursor()
    conn.select_db('sns')
    cur.execute('select id, nodeimportance from modify_scenes_v1')
    res = cur.fetchall()
    nodeImportance = {}
    sum=0
    for r in res:
        # sum=sum+float(r[1])
        nodeImportance[int(r[0])] = float(r[1])
    # nodeImportance[1]=nodeImportance[1]+(1-sum)
    conn.commit()
    conn.close()
    return nodeImportance


def getEdgeWeight():
    '''读取数据库获得边的权重，返回归一化之后的edgeImportance：dict{(from,to):weight}'''
    conn = getMySqlConn()
    cur = conn.cursor()
    conn.select_db('sns')
    cur.execute('select fromid, toid, edgeimportance from edgeimportance')
    res = cur.fetchall()
    edgeImportance = {}

    sum2 = 0
    for r in res:
        # if r[0] < r[1]:
        edgeImportance[(r[0], r[1])] = r[2]
        sum2 = sum2 + r[2]

    # for k, v in edgeImportance.items():
    #     edgeImportance[k] = v / sum2

    conn.commit()
    conn.close()
    return edgeImportance

def computePagerank():
    '''读取数据库并建立有向图，调用networkx计算pagerank值，返回pr：dict{id:pagerank}'''
    pk = 0
    elist = []
    G = nx.DiGraph()
    nodeImportance = getNodeWeight()
    edgeImportance = getEdgeWeight()
    for key, value in edgeImportance.items():
        # temp = key.split()
        fromNode = key[0]
        toNode = key[1]
        etruple = (int(fromNode), int(toNode), float(value))
        elist.append(etruple)
        # G.add_weighted_edges_from([(fromNode, toNode, value),])
    print elist
    G.add_weighted_edges_from(elist)
    pr = nx.pagerank(G, alpha=0.85, personalization=nodeImportance, nstart=nodeImportance,max_iter=1000)
    # pr = nx.pagerank(G, alpha=0.85)

    return pr


def savePr2db(pr):
    '''保存pagerank值到数据库中modify_scenes_v1的pagerank字段， pr:dict{id:pagerank}'''
    conn = getMySqlConn()
    cur = conn.cursor()
    conn.select_db('sns')
    for k, v in pr.items():
        try:
            cur.execute("update sns.modify_scenes_v1 set pagerank =" + str(v) +"where id = "+str(k))
        except:
            cur.execute("update sns.modify_scenes_v1 set pagerank =0 where id = "+str(k))
            continue

    conn.commit()
    conn.close()

if __name__ =='__main__':
    nodeImportance = getNodeWeight()
    sum = 0
    for k, v in nodeImportance.items():
        sum = sum + v
        #print k, v

    print "sum: " + str(sum)
    print "==========="
    sum2 = 0
    edgeImportance = getEdgeWeight()
    for k, v in edgeImportance.items():
        sum2 = sum2 + v
        #print k, v
    print "sum2: " + str(sum2)
    print len(edgeImportance) #1341
    pr = computePagerank()
    print "*" * 15
    print pr

    savePr2db(pr)

        # filename = 'CA-HepPh.txt'
        # G = nx.DiGraph()
        # # G = nx.Graph()
        #
        # with open(filename) as file:
        #
        #     for line in file:
        #         if "#" in line:
        #             continue
        #         head, tail = [int(x) for x in line.split()]
        #         G.add_edge(head, tail)
        #
        # pr = nx.pagerank(G, alpha=0.85)
        # print pr
        #
        # #将pagerank计算结果写入文件
        # f = open("pagerank-result-di.txt", 'wb+')
        # for key, value in pr.items():
        #     f.write(str(key)+"\t"+str(value)+"\n")
        # f.close()

